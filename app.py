from flask import Flask, request, render_template, redirect, url_for
from jd_summarizer import summarize_jd
from batch_processor import batch_process
from database import init_db
import os

app = Flask(__name__)

# Load settings from environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'data/cvs')  # <-- CHANGE HERE
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # <-- ADD SECRET KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY

# Initialize the database
init_db()

# Helper function to safely join lists into text
def safe_join(value):
    if isinstance(value, list):
        return " ".join(value)
    return value or ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    jd_text = request.form['jd']
    cvs = request.files.getlist('cvs')

    # Save uploaded CVs
    for cv in cvs:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], cv.filename)
        cv.save(filepath)

    # Summarize the JD
    summarized_jd = summarize_jd(jd_text)

    # Convert summarized JD (dict) to plain text safely
    summarized_jd_text = " ".join([
        "Skills: " + ", ".join(summarized_jd.get('skills', [])),
        "Experience: " + safe_join(summarized_jd.get('experience', '')),
        "Responsibilities: " + safe_join(summarized_jd.get('responsibilities', '')),
        "Qualifications: " + safe_join(summarized_jd.get('qualifications', ''))
    ])

    # Batch process CVs using the summarized JD text
    results = batch_process(cv_folder=app.config['UPLOAD_FOLDER'], jd_text=summarized_jd_text)

    # (Optional) Sort candidates by match score (best first)
    results = sorted(results, key=lambda x: x['match_score'], reverse=True)

    return render_template('results.html', candidates=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # <-- ADD PORT
    app.run(host='0.0.0.0', port=port, debug=True)  # <-- HOST + PORT
