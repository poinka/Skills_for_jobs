FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install flask pandas

CMD ["python3", "app.py"]