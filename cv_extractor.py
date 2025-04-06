import re
from pdfminer.high_level import extract_text

def extract_cv_data(file_path):
    text = extract_text(file_path)

    name = re.search(r'Name[:\s]*(\w+\s\w+)', text)
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    skills = re.search(r'Skills[:\s]*(.*)', text)
    experience = re.search(r'Experience[:\s]*(.*)', text)

    return {
        'name': name.group(1) if name else 'Unknown',
        'email': email.group(0) if email else 'Unknown',
        'skills': skills.group(1) if skills else '',
        'experience': experience.group(1) if experience else ''
    }
