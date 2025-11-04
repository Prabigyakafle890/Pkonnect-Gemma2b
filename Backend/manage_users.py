import sqlite3
import hashlib
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')

def get_connection():
    return sqlite3.connect(DATABASE)

def add_user(email, password, role, department):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password_hash, role, department) VALUES (?, ?, ?, ?)',
                       (email, password_hash, role, department))
        conn.commit()
        print(f"User {email} added successfully.")
    except sqlite3.IntegrityError:
        print(f"User {email} already exists.")
    conn.close()

def view_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, role, department FROM users')
    users = cursor.fetchall()
    conn.close()
    print("Users in database:")
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Department: {user[3]}")

def update_user(user_id, email=None, password=None, role=None, department=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    if email:
        updates.append('email = ?')
        params.append(email)
    if password:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        updates.append('password_hash = ?')
        params.append(password_hash)
    if role:
        updates.append('role = ?')
        params.append(role)
    if department:
        updates.append('department = ?')
        params.append(department)
    if updates:
        params.append(user_id)
        cursor.execute(f'UPDATE users SET {", ".join(updates)} WHERE id = ?', params)
        conn.commit()
        print(f"User ID {user_id} updated.")
    else:
        print("No updates specified.")
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    print(f"User ID {user_id} deleted.")
    conn.close()

if __name__ == "__main__":
    while True:
        print("\nUser Management Menu:")
        print("1. View Users")
        print("2. Add User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            view_users()
        elif choice == '2':
            email = input("Email: ")
            password = input("Password: ")
            role = input("Role (student/teacher/others): ")
            department = input("Department (BSC CSIT/BIT): ")
            add_user(email, password, role, department)
        elif choice == '3':
            user_id = int(input("User ID: "))
            email = input("New Email (leave blank to skip): ") or None
            password = input("New Password (leave blank to skip): ") or None
            role = input("New Role (leave blank to skip): ") or None
            department = input("New Department (leave blank to skip): ") or None
            update_user(user_id, email, password, role, department)
        elif choice == '4':
            user_id = int(input("User ID: "))
            delete_user(user_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
