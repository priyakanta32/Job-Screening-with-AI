import re

def summarize_jd(jd_text):
    def clean_split(text):
        return [item.strip() for item in text.split(',') if item.strip()]

    skills = re.findall(r'Skills?: (.+)', jd_text, re.I)
    experience = re.findall(r'Experience?: (.+)', jd_text, re.I)
    qualifications = re.findall(r'Qualifications?: (.+)', jd_text, re.I)
    responsibilities = re.findall(r'Responsibilities?: (.+)', jd_text, re.I)

    return {
        'skills': clean_split(skills[0]) if skills else [],
        'experience': experience[0].strip() if experience else '',
        'qualifications': clean_split(qualifications[0]) if qualifications else [],
        'responsibilities': clean_split(responsibilities[0]) if responsibilities else [],
    }
