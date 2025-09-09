from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime
import spacy

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Principal Info
principal_info = "Dr. B. A. Vishwanath – Principal, M.Sc, Ph.D."

# BCA Teachers
bca_teachers = [
    {"name": "Mrs. Sharada C", "qualification": "MCA, 20 years experience (Coordinator)"},
    {"name": "Mr. Jagadish Kotagi", "qualification": "MCA, 8 years experience (Academic Coordinator)"},
    {"name": "Mrs. Koteswari K", "qualification": "MCA, 4 years experience (Students Club Coordinator)"},
    {"name": "Ms. Preetha Sarathy P", "qualification": "MCA, 2.5 years experience"},
    {"name": "Mrs. Veena Revadi", "qualification": "M.Sc, 12 years experience"},
    {"name": "Ms. Sahana J K", "qualification": "MCA, 2 years experience (Project In-charge)"},
    {"name": "Mr. Pradeep B", "qualification": "MCA, 2 years experience (Placement Coordinator)"},  # ✅ Fixed comma
    {"name": "Mrs. Pranatheertha Jagadhish Aradhya", "qualification": "M.Sc, 25 years experience"},
    {"name": "Mrs. Madalambika K C", "qualification": "M.Sc, 2 years experience"},
    {"name": "Ms. Swetha Bai", "qualification": "M.Sc, 1 year experience"},
    {"name": "Ms. Pavithra R", "qualification": "M.Sc, 1 year experience"},
    {"name": "Ms. Akshatha B", "qualification": "M.Sc, 1 year experience"},
    {"name": "Vibha Desai", "qualification": "M.Sc, 3.2 years experience"},
    {"name": "Suhas Shreevathsa S", "qualification": "MCA, Fresher"}
]

# BBA Teachers
bba_teachers = [
    {"name": "Mrs. Ashwini Murthy", "qualification": "MBA, Coordinator / HOD"},
    {"name": "Mrs. Rani Prajwala", "qualification": "MBA, Assistant Professor"},
    {"name": "Ms. Sapna N", "qualification": "MBA, Assistant Professor"},
    {"name": "Mrs. Priya Upadhyay", "qualification": "MBA, Assistant Professor"},
    {"name": "Ms. ShivaShankari", "qualification": "MBA, Assistant Professor"},
    {"name": "Ms. Rakshitha S", "qualification": "MBA, Assistant Professor"},
    {"name": "Mr. Sohan Balaji", "qualification": "MBA, Assistant Professor"}
]

# NLP intent matcher using spaCy
def match_intent(user_input, keywords):
    doc1 = nlp(user_input)
    for keyword in keywords:
        doc2 = nlp(keyword)
        if doc1.similarity(doc2) > 0.75:  # spaCy similarity
            return True
        if keyword in user_input:  # fallback exact match
            return True
    return False

# Chatbot Logic
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    if not user_input:
        return "Please enter a message."

    if match_intent(user_input, ["hello", "hi", "hey"]):
        return "Hello! I am a bot for KLE Society's S. Nijalingappa College. How can I help you? (Type 'help' for options)"

    elif "help" in user_input:
        return ("You can ask about: about college, facilities, courses, subjects, teachers, principal, achievements, "
                "contact, placements, fees, student life, or type 'exit' to quit.")

    elif match_intent(user_input, ["principal", "head of college"]):
        return f"Our Principal is {principal_info}"

    elif "bca teacher" in user_input or "bca faculty" in user_input:
        response = "Here are some BCA faculty members with qualifications:\n"
        for t in bca_teachers:
            response += f"- {t['name']} – {t['qualification']}\n"
        return response

    elif "bba teacher" in user_input or "bba faculty" in user_input:
        response = "Here are some BBA faculty members with qualifications:\n"
        for t in bba_teachers:
            response += f"- {t['name']} – {t['qualification']}\n"
        return response

    elif any(course in user_input for course in ["bcom", "b.sc", "bsc", "ba", "mca", "mcom", "ma", "msc"]):
        return "The faculty for this course are well-qualified (usually holding Master’s or higher) and experienced in their subjects."

    elif match_intent(user_input, ["about college", "about nijalingappa"]):
        return ("K.L.E. Society’s S. Nijalingappa College was established in 1963 and is known for academic excellence...")

    elif match_intent(user_input, ["facilities", "infrastructure", "campus"]):
        return ("The college campus is spread over 1.72 acres with well-equipped labs, library, auditorium, and more...")

    elif match_intent(user_input, ["courses", "programs"]):
        return ("KLESNC offers a variety of UG and PG programs including BCA, BBA, B.Com, B.Sc, BA, MCA, M.Com, MA, and MSc.")

    elif "subjects" in user_input:
        if "bca" in user_input:
            return "The BCA program follows Bengaluru City University curriculum with Computer Science core subjects."
        elif "bba" in user_input:
            return "The BBA program covers Management, Accounting, Marketing, and Business Analytics."
        elif "bcom" in user_input:
            return "The B.Com program includes subjects like Accounting, Taxation, and Finance."
        elif "bsc" in user_input:
            return "The B.Sc program varies by combinations like PCM, CBZ, etc."
        elif "ba" in user_input:
            return "The BA program includes History, Economics, Psychology, Political Science, and Optional English."
        elif "msc" in user_input:
            return "The MSc program includes advanced topics in Biotechnology, Mathematics, etc."
        elif "mca" in user_input:
            return "The MCA program covers software engineering, AI, databases, and web development."
        elif "mcom" in user_input:
            return "The M.Com program covers advanced commerce, finance, and accounting topics."
        elif "ma" in user_input:
            return "The MA in English program includes Literature, Linguistics, and Critical Theory."
        else:
            return "Please specify the course (e.g., 'BCA subjects', 'BBA subjects')."

    elif match_intent(user_input, ["achievements", "accreditation"]):
        return "KLESNC is NAAC accredited with 'A' grade and has received numerous awards for academic excellence."

    elif match_intent(user_input, ["placements", "placement"]):
        return "The Placement Cell has strong industry ties and provides training and job opportunities."

    elif match_intent(user_input, ["fees", "fee structure"]):
        return "The annual fee structure varies by course. Please contact the office for details."

    elif match_intent(user_input, ["student life", "extracurriculars", "clubs"]):
        return "Student life is vibrant with cultural fests, clubs, NSS, NCC, sports, and more."

    elif match_intent(user_input, ["contact", "address", "location"]):
        return ("Contact Details:\nKLE Society’s S. Nijalingappa College\n"
                "#1040, II Block, Rajajinagar, Bangalore – 560 010")

    elif match_intent(user_input, ["exit", "quit"]):
        return "Goodbye! Have a great day!"

    else:
        return "Sorry, I don't have that information. Please try something else or type 'help'."

# Flask Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})

@app.route("/save_info", methods=["POST"])
def save_info():
    data = request.get_json()
    name = data.get("user_name")
    course = data.get("course_interest")
    mobile = data.get("mobile_number")
    pu_marks = data.get("pu_marks", "")
    ug_percentage = data.get("ug_percentage", "")

    file_exists = False
    try:
        with open("student_data.csv", "r", newline="", encoding="utf-8") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open("student_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "PU Marks", "UG Percentage/CGPA", "Mobile", "Course"])
        writer.writerow([datetime.now(), name, pu_marks, ug_percentage, mobile, course])

    return jsonify({"status": "success", "message": "Info saved successfully!"})

@app.route("/view_students")
def view_students():
    students = []
    try:
        with open("student_data.csv", mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        pass
    return render_template('view_student.html', students=students)

if __name__ == "__main__":
    app.run(debug=True)
