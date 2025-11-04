import sqlite3
import hashlib
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')

def add_user(email, password, role, department):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password_hash, role, department) VALUES (?, ?, ?, ?)',
                       (email, password_hash, role, department))
        conn.commit()
        print(f"User {email} added successfully.")
    except sqlite3.IntegrityError:
        print(f"User {email} already exists.")
    conn.close()

if __name__ == "__main__":
    # Example: Add a new user
    add_user('newstudent@pkonnect.edu.np', 'newpassword', 'student', 'BSC CSIT')
