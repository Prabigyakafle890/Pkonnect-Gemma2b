from app.ollama_proxy import query_ollama
from app.dataloader import load_department_data, search_data
import re

def extract_keywords(message):
    """
    Extract keywords from the message by splitting into words and filtering out common stop words.
    """
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'this', 'that', 'these', 'those', 'what', 'who', 'where', 'when', 'why', 'how', 'and', 'or', 'but', 'if', 'then', 'else', 'for', 'to', 'from', 'in', 'on', 'at', 'by', 'with', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'of', 'off', 'out', 'over', 'under', 'again', 'further', 'then', 'once'}
    words = re.findall(r'\b\w+\b', message.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

def get_response(message, user_type='guest', department=None, role=None):
    if user_type == 'guest':
        # Guest bot: limited info, uses Ollama
        return query_ollama(message)
    elif user_type == 'student':
        # Institutional bot: department-specific, role-based, uses Ollama with context
        if department in ['BSC CSIT', 'BIT']:
            # Load department data
            data = load_department_data(department)
            # Extract keywords from message
            keywords = extract_keywords(message)
            # Search for matching data with full query for better name matching
            matches = search_data(data, keywords, message)
            # Prepare context from matches
            context = ""
            if matches:
                context = "Relevant data from our records:\n"
                for match in matches[:5]:  # Limit to top 5 matches
                    # Check if it's teacher data (has 'name_of_teacher') or student data (has 'Nameof students')
                    if 'name_of_teacher' in match:
                        teacher_name = match.get('name_of_teacher', 'N/A')
                        subject = match.get('subject', 'N/A')
                        semester = match.get('semester', 'N/A')
                        designation = match.get('designation', 'N/A')
                        context += f"- Teacher: {teacher_name}, Subject: {subject}, Semester: {semester}, Designation: {designation}\n"
                    elif 'Nameof students' in match:
                        student_name = match.get('Nameof students', 'N/A')
                        roll_no = match.get('Roll. No.', 'N/A')
                        email = match.get('Email', 'N/A')
                        district = match.get('District', 'N/A')
                        province = match.get('Province', 'N/A')
                        context += f"- Student: {student_name}, Roll No: {roll_no}, Email: {email}, District: {district}, Province: {province}\n"
                    else:
                        # Fallback for other data types
                        context += f"- Record: {str(match)}\n"
                context += "\nUse this data to answer the user's question accurately. Provide clean, concise information without unnecessary details.\n"
            # Append context to message
            enhanced_message = context + message
            return query_ollama(enhanced_message, department=department, role=role)
        else:
            return "Invalid department."
    else:
        return "Invalid user type."
