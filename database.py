import sqlite3

def init_db():
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            match_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_candidate_data(candidate):
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO candidates (name, email, match_score) 
        VALUES (?, ?, ?)
    ''', (candidate['name'], candidate['email'], candidate['match_score']))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates')
    data = cursor.fetchall()
    conn.close()
    return data
