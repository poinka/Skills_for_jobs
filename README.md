# Habr Career Tech Job Dashboard

A Flask-based web application that visualizes tech job data from Habr Career using D3.js. The dashboard features interactive charts with a soft, girly pastel pink aesthetic, showcasing job categories, technical skills, experience levels, and skills by job category.

## Features

- **Interactive Charts**:
  - **Job Categories**: Pie chart displaying the distribution of job categories (e.g., Software Development, Analytics).
  - **Top 10 Technical Skills**: Bar chart of the most common technical skills across all jobs.
  - **Experience Levels**: Pie chart of experience levels (e.g., Средний (Middle), Старший (Senior)).
  - **Skills by Category**: Bar charts for top skills in Software Development, Analytics, Information Security, and Artificial Intelligence.
- **Design**: Soft pastel pink color scheme with fade-in animations, hover tooltips, and a responsive layout.
- **Technologies**: Built with Flask (backend), D3.js (visualizations), Bootstrap (styling), and Inter font for a modern, clean look.

## Setup

### Prerequisites
- Python 3.6 or higher
- Git
- A web browser (e.g., Chrome, Firefox)

### Installation (local setup)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/poinka/Skills_for_jobs.git
   cd Skills_for_jobs
   ```
2. **Install Dependencies**:
    ```bash
    pip install flask pandas
    ```

3. **Ensure Data File**:
Verify that *cleaned_jobs.json* is in the project root. This file contains the job data used by the dashboard.


### Running the App (local setup)
1. **Start the Flask Server**:
```bash
    python app.py
```
2. **Access the Dashboard**:
- Open a browser and visit http://localhost:5000.
- Explore the charts, which load data from cleaned_jobs.json via API endpoints.

### Docker Setup
1. Install Docker Desktop
2. Clone the Repository (if not already done):
```bash
git clone https://github.com/poinka/Skills_for_jobs.git
cd Skills_for_jobs
```
3. Build the Docker Image:
```bash
docker-compose build
```

4. Run the Docker Container:
```bash
docker-compose up
```
The app will be available at http://localhost:5000.

Press Ctrl+C to stop the container.

## Usage
- **View Charts**: Navigate to http://localhost:5000 to see the dashboard.
- **Overview Section**: Includes Job Categories, Top 10 Technical Skills, and Experience Levels.
- **Skills Section**: Shows technical skills for Software Development, Analytics, Information Security, and Artificial Intelligence.
- **Interact**: Hover over chart elements to see tooltips with data details.
Debug: Open the browser’s Developer Tools (F12) and check the Console for data logs (e.g., “Categories data”, “Experience data”).

## Technologies
- **Flask**: Python web framework for the backend and API endpoints.
- **D3.js**: JavaScript library for interactive data visualizations.
- **Bootstrap**: CSS framework for responsive layout and styling.
- **Inter Font**: Modern, clean font for typography.
- **Pandas**: Python library for data processing.

## Data Source
The dashboard uses cleaned_jobs.json, which contains cleaned job data from **Habr Career**. The data includes:

- **Categories**: Job categories (e.g., Software Development, Analytics).
- **Technical Skills**: Skills required for jobs (e.g., JavaScript, Python).
- **Experience Levels**: Levels like Средний (Middle), Старший (Senior).

Built with 💖 by poinka. Powered by Flask & D3.js.