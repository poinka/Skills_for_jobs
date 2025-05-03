import scrapy
import uuid
from urllib.parse import urljoin
from scrapy.http import Request

class HabrSpider(scrapy.Spider):
    name = 'parse_jobs'
    allowed_domains = ['career.habr.com']
    start_urls = [
        'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=4&s[]=82&s[]=72&s[]=5&s[]=75&s[]=6&s[]=1&s[]=77&s[]=7&s[]=83&s[]=84&s[]=73&s[]=8&s[]=85&s[]=86&s[]=188&s[]=178&s[]=106&s[]=78&s[]=21&s[]=172&s[]=174&s[]=79&s[]=173&s[]=80&s[]=176&s[]=81&s[]=118&s[]=182&s[]=44&s[]=125&s[]=177&s[]=175&s[]=126&s[]=98&s[]=41&s[]=42&s[]=99&s[]=168&s[]=43&s[]=76&s[]=96&s[]=97&s[]=95&s[]=100&s[]=133&s[]=111&type=all'
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'FEEDS': {
            'habr_jobs.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
            }
        },
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        },
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [403, 429],
        'ROBOTSTXT_OBEY': False,  # Check Habr's terms
    }
    job_count = 0
    max_jobs = 1500

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, meta={'dont_redirect': False})

    def parse(self, response):
        if response.status in [403, 429]:
            self.logger.error(f"Received {response.status} on {response.url}. Check bot detection.")
            return

        # Extract job cards
        job_cards = response.css('div.vacancy-card')
        if not job_cards:
            self.logger.warning(f"No job cards found on {response.url}. Check HTML structure.")
            self.logger.debug(f"Response body: {response.text[:1000]}")

        for job in job_cards:
            if self.job_count >= self.max_jobs:
                return

            job_link = job.css('a.vacancy-card__title-link::attr(href)').get()
            if job_link:
                self.job_count += 1
                full_link = urljoin('https://career.habr.com', job_link)
                job_data = self.extract_job_data(job)
                yield Request(full_link, callback=self.parse_job, meta={'job_data': job_data})

        # Follow pagination
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page and self.job_count < self.max_jobs:
            next_page_url = urljoin('https://career.habr.com', next_page)
            yield Request(next_page_url, callback=self.parse, meta={'dont_redirect': False})

    def extract_job_data(self, job):
        """Extract data from job card, including skills."""
        company = job.css('div.vacancy-card__company-title a::text').get(default='N/A').strip()
        company_link = job.css('div.vacancy-card__company-title a::attr(href)').get(default='N/A')
        company_link = urljoin('https://career.habr.com', company_link) if company_link != 'N/A' else 'N/A'
        title = job.css('a.vacancy-card__title-link::text').get(default='N/A').strip()
        work_format = job.css('div.vacancy-card__meta span::text').get(default='N/A').strip()
        skills = job.css('div.vacancy-card__skills a.link-comp::text').getall()
        skills = [skill.strip() for skill in skills if skill.strip()]

        return {
            'company': company,
            'company_link': company_link,
            'title': title,
            'work_format': work_format,
            'skills': skills
        }

    def parse_job(self, response):
        job_data = response.meta['job_data']

        yield {
            'id': str(uuid.uuid4()),
            'title': job_data['title'],
            'company': job_data['company'],
            'url': response.url,
            'company_link': job_data['company_link'],
            'work_format': job_data['work_format'],
            'skills': job_data['skills']
        }