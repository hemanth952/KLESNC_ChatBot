from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime
import re
import os
import uuid
import pyttsx3  # ✅ Replaced gTTS with pyttsx3

app = Flask(__name__)

# ---------------- DATA ---------------- #
# Principal Info
principal_info = "Dr. Arunkumar B. Sonappanavar –  M.Sc, Ph.D."

# BCA Teachers
bca_teachers = [
    {"name": "Mrs. Sharada C", "qualification": "MCA, 20 years experience (Coordinator)"},
    {"name": "Mr. Jagadish Kotagi", "qualification": "MCA, 8 years experience (Academic Coordinator)"},
    {"name": "Mrs. Koteswari K", "qualification": "MCA, 4 years experience (Students Club Coordinator)"},
    {"name": "Ms. Preetha Sarathy P", "qualification": "MCA, 2.5 years experience"},
    {"name": "Mrs. Veena Revadi", "qualification": "M.Sc, 12 years experience"},
    {"name": "Ms. Sahana J K", "qualification": "MCA, 2 years experience (Project In-charge)"},
    {"name": "Mr. Pradeep B", "qualification": "MCA, 2 years experience (Placement Coordinator)"},
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

# ---------------- INTENT PATTERNS ---------------- #
patterns = {
    "greet": re.compile(r'\b(hello|hi|hey|welcome)\b', re.I),
    "help": re.compile(r'\b(help|options|what can you do)\b', re.I),
    "principal": re.compile(r'\b(principal|head of college|hod)\b', re.I),
    "courses": re.compile(r'\b(courses|programs|departments|offerings)\b', re.I),
    "facilities": re.compile(r'\b(facilities|infrastructure|campus|labs|library|auditorium)\b', re.I),
    "achievements": re.compile(r'\b(achievement|achievements|accreditation|naac|rank|ranking|award|awards)\b', re.I),
    "placements": re.compile(r'\b(placement|placements|jobs|recruitment|career)\b', re.I),
    "fees": re.compile(r'\b(fee|fees|fee structure|cost|tuition)\b', re.I),
    "student_life": re.compile(r'\b(student life|extracurricular|fest|festival|clubs|nss|ncc|sports)\b', re.I),
    "why_kle": re.compile(r'\b(why choose kle|why kle|advantages|benefits)\b', re.I),
    "bca_teachers": re.compile(r'\b(bca teachers|bca faculty)\b', re.I),
    "bba_teachers": re.compile(r'\b(bba teachers|bba faculty)\b', re.I),
    "teachers": re.compile(r'\b(teachers|faculty|staff|professor|lecturer)\b', re.I),
    "contact": re.compile(r'\b(contact|address|location|phone|email)\b', re.I),
    "exit": re.compile(r'\b(exit|quit|bye|goodbye)\b', re.I),
}

# ---------------- RESPONSES ---------------- #
responses = {
    "greet": "👋 Hello! I am the chatbot for KLE Society's S. Nijalingappa College (KLESNC). How can I help you? (Type 'help' for options)",
    "help": (
        "📌 You can ask me about:\n"
        "- Principal\n"
        "- Courses\n"
        "- Facilities\n"
        "- Achievements\n"
        "- Placements\n"
        "- Fees\n"
        "- Teachers / Faculty (BCA or BBA)\n"
        "- Student Life\n"
        "- Why Choose KLE\n"
        "- Contact\n"
        "\nOr type 'exit' to quit."
    ),
    "principal": f"🎓 Our Principal is {principal_info}.",
    "courses": (
        "📚 Courses Offered:\n"
        "- BCA (Computer Applications)\n"
        "- BBA (Business Administration)\n"
        "- B.Com (Commerce)\n"
        "- B.Sc (Science combinations)\n"
        "- BA (Arts)\n"
        "- MCA (Computer Applications - PG)\n"
        "- M.Com (Commerce - PG)\n"
        "- MA (English)\n"
        "- MSc (Biotech, Mathematics, etc.)"
    ),
    "facilities": (
        "🏫 Facilities:\n"
        "> ICT Enabled Classrooms & Labs\n"
        "> Digitalized, well-stacked library with ILMS spread across three floors\n"
        "> AV-Studio Facility\n"
        "> Women Anti-Harassment & Grievance Redressal Cell\n"
        "> Campus Health Centre\n"
        "> Bank\n"
        "> Cafeteria\n"
        "> Lounge for Girl Students\n"
        "> Auditoriums & Open-Air Theatre\n"
        "> Wi-Fi Campus, Computer & Language Labs\n"
        "> NCC, NSS, YRC, Dept Clubs,\n"
        "> Forums & Student Council\n"
        "> CCTV Surveillance 24/7\n"
        "> In-House Sports Complex & Cardio\n"
        "> Outdoor Playground & Indoor Game Facilities"
    ),
    "achievements": (
        "🏅 Achievements:\n"
        "- NAAC Accredited with 'A' Grade\n"
        "- Ranked among top colleges under Bengaluru City University\n"
        "- Award-winning research and student projects\n"
        "- Active NSS, NCC, and cultural participation\n"
        "- Alumni excelling in IT, Business, and Government sectors"
    ),
    "placements": (
        "💼 Placements:\n"
        "- Dedicated Placement Cell with strong industry ties\n"
        "- Companies like Infosys, Wipro, TCS, Accenture visit for recruitment\n"
        "- Training in Aptitude, Soft Skills, and Interview Preparation\n"
        "- Internship opportunities for UG & PG students"
    ),
    "fees": (
        "💰 Fee Structure (approx per year):\n"
        "- BCA: ₹1,05,000 to ₹1,20,000\n"
        "- BBA: ₹1,10,000 to ₹1,25,000\n"
        "- B.Com: ₹30,000 to ₹40,000\n"
        "- BA / B.Sc: ₹25,000 to ₹35,000\n"
        "- PG Programs (MCA, M.Com, MSc, MA): ₹50,000 to ₹70,000\n"
        "👉 For exact details, please contact the college office."
    ),
    "teachers": (
        "👩‍🏫 Faculty at KLESNC:\n"
        "- Highly qualified professors with MSc, MCA, MBA, and PhD degrees\n"
        "- Experienced staff in Computer Science, Commerce, Management, Arts, and Sciences\n"
        "- Dedicated coordinators for Placements, Clubs, and Student Development\n\n"
        "👉 You can also ask specifically for BCA teachers or BBA teachers."
    ),
    "contact": (
        "📍 Contact:\n"
        "KLE Society’s S. Nijalingappa College\n"
        "#1040, II Block, Rajajinagar, Bangalore – 560010\n"
        "📞 Phone: +91-80-2332XXXX\n"
        "📧 Email: info@klesnc.edu"
    ),
    "student_life": (
        "🎉 Student Life:\n"
        "- Annual cultural fest and inter-collegiate competitions\n"
        "- NSS & NCC for social service and discipline\n"
        "- Active student clubs (IT Club, Management Club, Cultural Club)\n"
        "- Sports teams in cricket, basketball, football, athletics\n"
        "- Vibrant campus life with seminars, workshops, and guest lectures"
    ),
    "why_kle": (
        "🌟 Why Choose KLE SNC?\n"
        "- 100% Placement Assistance\n"
        "- Skill Enhancement Short Term Courses & Certifications\n"
        "- Pre-Placement and Soft Skills Training\n"
        "- Internships, Projects & Field Works\n"
        "- Institute/Industrial Visits, Study Tours & Excursions\n"
        "- Inter & Intra-Collegiate Events: Fests, Fairs, Exhibitions & Competitions\n"
        "- Seminars & Invited Guest Lectures\n"
        "- Hands-on Training & Interactive Workshops\n"
        "- Competitive Examination Coaching"
    ),
    "exit": "👋 Goodbye! Have a great day!",
}

# ---------------- BOT LOGIC ---------------- #
def get_bot_response(user_input):
    text = user_input.strip().lower()
    if not text:
        return "⚠ Please enter a message."
    
    matched_intents = []
    for key, pattern in patterns.items():
        if pattern.search(text):
            matched_intents.append(key)
    
    if not matched_intents:
        return "❓ Sorry, I don't have that information. Type 'help' to see what I can do."

    intent = matched_intents[0]

    if intent == "bca_teachers":
        response = "👩‍💻 BCA Department Faculty:\n"
        for t in bca_teachers:
            response += f"- {t['name']} – {t['qualification']}\n"
        return response.strip()

    if intent == "bba_teachers":
        response = "📊 BBA Department Faculty:\n"
        for t in bba_teachers:
            response += f"- {t['name']} – {t['qualification']}\n"
        return response.strip()

    return responses.get(intent, "❓ Sorry, I don't have that information.")

# ---------------- FLASK ROUTES ---------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)

    # ---------- pyttsx3 VOICE GENERATION ----------
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index for male/female voices
    engine.setProperty('rate', 170)  # Speaking speed

    filename = f"static/{uuid.uuid4()}.mp3"
    engine.save_to_file(bot_reply, filename)
    engine.runAndWait()

    return jsonify({"response": bot_reply, "voice": filename})

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

# ---------------- RUN APP ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
