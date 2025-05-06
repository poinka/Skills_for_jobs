from flask import Flask, jsonify, render_template
import pandas as pd
from collections import Counter
import json

app = Flask(__name__)

# Load cleaned JSON data
file_path = "cleaned_jobs.json"
df = pd.read_json(file_path)

# Aggregate data
def aggregate_data():
    # Job categories
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    category_data = category_counts.to_dict(orient='records')

    # Top 10 technical skills overall
    all_skills = [skill for skills in df['skills'] for skill in skills]
    skill_counts = Counter(all_skills).most_common(10)
    skills_data = [{'skill': skill, 'count': count} for skill, count in skill_counts]

    # Experience levels
    experience_counts = df['level'].value_counts().reset_index()
    experience_counts.columns = ['level', 'count']
    experience_data = experience_counts.to_dict(orient='records')

    # Technical skills per category
    categories = ['Software Development', 'Analytics', 'Information Security', 'Artificial Intelligence', 'Other']
    skills_per_category = {}
    for category in categories:
        category_df = df[df['category'] == category]
        category_skills = [skill for skills in category_df['skills'] for skill in skills]
        category_skill_counts = Counter(category_skills).most_common(10)
        skills_per_category[category] = [{'skill': skill, 'count': count} for skill, count in category_skill_counts]

    return {
        'categories': category_data,
        'skills': skills_data,
        'experience': experience_data,
        'skills_per_category': skills_per_category
    }

# Store aggregated data
data = aggregate_data()

# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/categories')
def get_categories():
    return jsonify(data['categories'])

@app.route('/api/skills')
def get_skills():
    return jsonify(data['skills'])

@app.route('/api/experience')
def get_experience():
    return jsonify(data['experience'])

@app.route('/api/skills_per_category')
def get_skills_per_category():
    return jsonify(data['skills_per_category'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)