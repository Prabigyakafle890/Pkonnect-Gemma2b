import sqlite3
import hashlib
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'users.db')

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    # Insert sample users
    sample_users = [
        ('student1@pkonnect.edu.np', 'password123', 'student', 'BSC CSIT'),
        ('student2@pkonnect.edu.np', 'password123', 'student', 'BIT'),
        ('teacher1@pkonnect.edu.np', 'password123', 'teacher', 'BSC CSIT'),
        ('other1@pkonnect.edu.np', 'password123', 'others', 'BIT'),
    ]
    for email, password, role, dept in sample_users:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO users (email, password_hash, role, department) VALUES (?, ?, ?, ?)',
                           (email, password_hash, role, dept))
        except sqlite3.IntegrityError:
            pass  # User already exists
    conn.commit()
    conn.close()

def verify_user(email, password, role, department):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password_hash = ? AND role = ? AND department = ?',
                   (email, password_hash, role, department))
    user = cursor.fetchone()
    conn.close()
    return user is not None
