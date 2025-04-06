from cv_extractor import extract_cv_data
from matcher import match_cv_to_jd
from scheduler import schedule_interview
from database import save_candidate_data
import os

def batch_process(cv_folder, jd_text):
    results = []

    for cv_file in os.listdir(cv_folder):
        if cv_file.endswith('.pdf'):
            cv_path = os.path.join(cv_folder, cv_file)
            cv_data = extract_cv_data(cv_path)
            cv_text = ' '.join(str(value) for value in cv_data.values())

            match_score = match_cv_to_jd(cv_text, jd_text)

            # Smart fallback for name guessing
            name = cv_data.get('name')
            email = cv_data.get('email', 'Unknown')

            if not name and email != 'Unknown':
                name_guess = email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
            else:
                name_guess = name or 'Unknown'

            candidate = {
                'name': name_guess,
                'email': email,
                'match_score': match_score
            }

            # Save to database
            save_candidate_data(candidate)

            # Shortlist candidates above threshold
            if match_score >= 80:
                schedule_interview(candidate)

            results.append(candidate)

    # OPTIONAL: After processing, delete uploaded CVs to prevent duplicates
    for cv_file in os.listdir(cv_folder):
        file_path = os.path.join(cv_folder, cv_file)
        os.remove(file_path)

    return results
