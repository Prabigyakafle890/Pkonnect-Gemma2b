from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.ollama_proxy import query_ollama
from app.db import verify_user
import requests
import re

chatbot_bp = Blueprint('chatbot_bp', __name__)

# Home page
@chatbot_bp.route("/")
def home():
    return render_template("index.html")

# Guest page
@chatbot_bp.route("/guest")
def guest():
    return render_template("guest.html")

# Chatbot page
@chatbot_bp.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# Select Department
@chatbot_bp.route('/select-department', methods=['GET', 'POST'])
def select_department():
    if request.method == 'POST':
        department = request.form.get('department')
        if department:
            session['department'] = department
            return redirect(url_for('chatbot_bp.select_role'))
    return render_template('department_select.html')

# Select Role
@chatbot_bp.route('/select-role', methods=['GET', 'POST'])
def select_role():
    if request.method == 'POST':
        role = request.form.get('role')
        if role:
            session['role'] = role
            return redirect(url_for('chatbot_bp.institution_login'))
    return render_template('role_select.html')

# Institution Login
@chatbot_bp.route('/institution-login', methods=['GET', 'POST'])
def institution_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        department = session.get('department')
        role = session.get('role')
        if not department or not role:
            error = "Session expired. Please start over."
        elif re.match(r'^[a-z0-9._%+-]+@pkonnect\.edu\.np$', email) and password:
            if verify_user(email, password, role, department):
                session['user_email'] = email
                session['is_student'] = True
                return redirect(url_for('chatbot_bp.student'))
            else:
                error = "Invalid credentials."
        else:
            error = "Invalid email or password."
    return render_template('institution_login.html', error=error)

# Student page
@chatbot_bp.route('/student')
def student():
    if not session.get('is_student'):
        return redirect(url_for('chatbot_bp.select_department'))
    return render_template('chatbot.html', user_type='student')

# Google Sign-In callback
@chatbot_bp.route('/signin/callback', methods=['POST', 'GET'])
def google_callback():
    # Google sends the ID token as a POST parameter named 'credential'
    token = request.form.get('credential') or request.json.get('credential')
    if not token:
        return "Missing credential", 400

    # Verify token with Google
    google_resp = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    if google_resp.status_code != 200:
        return "Invalid token", 400

    user_info = google_resp.json()
    # Save user info in session
    session['user_email'] = user_info.get('email')
    session['user_name'] = user_info.get('name')
    # Redirect to chatbot or dashboard
    return redirect(url_for('chatbot_bp.chatbot'))

# Chat endpoint
@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'response': 'No message provided.'}), 400

        user_type = 'guest'
        department = None
        role = None
        if session.get('is_student'):
            user_type = 'student'
            department = session.get('department')
            role = session.get('role')

        from app.chatbot import get_response
        response = get_response(message, user_type, department, role)
        return jsonify({'response': response})

    except Exception as e:
        print("❌ Chat route error:", e)
        return jsonify({'response': 'Internal server error occurred.'}), 500

# History endpoint (no DB, returns empty)
@chatbot_bp.route('/history', methods=['GET'])
def history():
    return jsonify({'history': []})


@chatbot_bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        # Replace with your college's domain
        if re.match(r'^[a-z0-9._%+-]+@pkonnect\.edu\.np$', email):
            session['user_email'] = email
            session['is_student'] = True
            return redirect(url_for('chatbot_bp.student'))
        else:
            error = "Please enter a valid college student email."
    return render_template('institution_login.html', error=error)