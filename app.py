from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

# Replace with your chatbot logic
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    if not user_input:
        return "Please enter a message."
    if any(greet in user_input for greet in ["hello", "hi", "hey"]):
        return "Hello! I am a bot for KLE Society's S. Nijalingappa College. How can I help you? (Type 'help' for options)"
    elif "help" in user_input:
        return "You can ask about: about college, facilities, courses, specific subjects (e.g., 'BCA subjects'), achievements, contact, placements, fees, student life, or type 'exit' to quit."
    elif "about college" in user_input or "about nijalingappa" in user_input:
        return ("K.L.E. Society’s S. Nijalingappa College was established in 1963. It is a premier institution of the K.L.E. Society, starting as a science college on MG Road before moving to its current Rajajinagar campus in 1966. The college is permanently affiliated with Bengaluru City University and is committed to providing quality education to over 3000 students from diverse backgrounds.")
    elif "facilities" in user_input or "infrastructure" in user_input or "campus" in user_input:
        return ("The college campus is spread over 1.72 acres and is designed to support academic and personal growth.\n\n"
                "Key Facilities:\n"
                "- Library: A spacious and centralized library with over 66,000 books, journals, and digital resources. It is fully automated and provides a quiet space for study.\n"
                "- Labs: Well-equipped labs for all science departments (Physics, Chemistry, Biotechnology), a dedicated Language Lab, a CAD Lab, and multiple Computer Labs with a 1:1 student-to-computer ratio.\n"
                "- Sports: A wide range of indoor and outdoor sports facilities, including grounds for cricket, football, basketball, and a gymnasium with modern equipment.\n"
                "- Hostel: Separate off-campus hostel facilities for both male and female students with all essential amenities.\n"
                "- Other Amenities: The campus is fully Wi-Fi-enabled and features a hygienic cafeteria, a health center with a medical officer, a Canara Bank extension counter, and photocopying facilities.")
    elif "courses" in user_input or "programs" in user_input:
        return ("KLESNC offers a variety of courses:\n\n"
                "Undergraduate Programs:\n"
                "- B.Sc (Physics, Chemistry, Mathematics; Chemistry, Botany, Zoology; Physics, Mathematics, Computer Science; Fashion & Apparel Design)\n"
                "- B.A. (History, Economics, Political Science; Journalism, Psychology, Political Science)\n"
                "- B.Com (Regular, Business Data Analytics, Chartered Accountancy, Company Secretary)\n"
                "- BCA, BBA (Regular & Aviation), BHM, BTTM\n\n"
                "Postgraduate Programs:\n"
                "- M.Sc (Physics, Chemistry, Mathematics)\n"
                "- MCA, M.Com, MA (English), MTA\n\n"
                "The college also offers various add-on courses in fields like cloud services, foreign languages, and more.")
    
    # 🔹 Subjects handling for all courses
    elif "subjects" in user_input:
        if "bca" in user_input:
            return ("The BCA program at KLESNC follows Bengaluru City University curriculum.\n\n"
                    "Core Subjects:\n"
                    "- Programming: C, C++, Java, Python\n"
                    "- Data & Systems: Data Structures, DBMS, Operating Systems\n"
                    "- Web & Networks: HTML, CSS, JavaScript, Networks, Cryptography\n"
                    "- Others: Discrete Math, Software Engineering, AI, ML\n"
                    "Also includes certificate courses in AWS, RPA, Cyber Security.")
        elif "bba" in user_input:
            return ("The BBA program covers:\n"
                    "- Principles of Management, Business Economics, Financial Accounting\n"
                    "- HR Management, Marketing, Business Law, Organizational Behavior\n"
                    "- Banking, Insurance, Entrepreneurship, Business Analytics")
        elif "bcom" in user_input:
            return ("The B.Com program includes:\n"
                    "- Financial Accounting, Corporate Accounting, Business Law\n"
                    "- Cost Accounting, Income Tax, Auditing, Management Accounting\n"
                    "- Banking, Company Law, Business Communication, Statistics")
        elif "bsc" in user_input:
            return ("The B.Sc program varies by combination:\n"
                    "- PCM: Physics, Chemistry, Mathematics\n"
                    "- CBZ: Chemistry, Botany, Zoology\n"
                    "- PMCs: Physics, Mathematics, Computer Science\n"
                    "- Fashion & Apparel Design: Textile Science, Fashion Illustration, CAD, Apparel Production")
        elif "ba" in user_input:
            return ("The BA program includes:\n"
                    "- History, Economics, Political Science\n"
                    "- Journalism, Psychology, Political Science\n"
                    "- Courses emphasize social sciences, humanities, and communication.")
        elif "msc" in user_input:
            return ("The MSc program includes:\n"
                    "- Physics: Quantum Mechanics, Electrodynamics, Solid State Physics\n"
                    "- Chemistry: Organic, Inorganic, Physical, Analytical Chemistry\n"
                    "- Mathematics: Algebra, Analysis, Topology, Differential Equations")
        elif "mca" in user_input:
            return ("The MCA program covers:\n"
                    "- Advanced Programming (Java, Python, C#)\n"
                    "- DBMS, Cloud Computing, Big Data Analytics\n"
                    "- AI, ML, IoT, Web & Mobile App Development\n"
                    "- Software Project Management")
        elif "mcom" in user_input:
            return ("The M.Com program covers:\n"
                    "- Advanced Financial Accounting, Corporate Tax Planning\n"
                    "- Business Research Methods, International Business\n"
                    "- Strategic Management, Financial Management")
        elif "ma" in user_input:
            return ("The MA in English program includes:\n"
                    "- British Literature, American Literature, Indian Writing in English\n"
                    "- Literary Criticism, Linguistics, Cultural Studies, Research Methodology")
        else:
            return "Please specify the course (e.g., 'BCA subjects', 'BBA subjects', 'B.Com subjects')."
    
    elif "achievements" in user_input or "accreditation" in user_input:
        return ("KLE Society's S. Nijalingappa College has a long history of excellence.\n"
                "- NAAC 'A+' Grade: CGPA of 3.82 on a 4-point scale, one of the highest in Karnataka.\n"
                "- UGC Status: Recognized as a 'College with Potential for Excellence' (CPE).\n"
                "- Awards: Numerous rank holders, gold medalists, and state/national level achievers in cultural, literary, and sports events.")
    elif "placements" in user_input or "placement" in user_input:
        return ("The Placement Cell at KLESNC has strong industry collaborations.\n"
                "- Median Package (2024): UG – INR 3.0 LPA, PG – INR 3.50 LPA\n"
                "- Top Recruiters: Infosys, Wipro, TCS, Deloitte, IBM, L&T, Amazon, Cognizant, Gallagher\n"
                "- Training: Placement training, aptitude workshops, mock interviews")
    elif "fees" in user_input or "fee structure" in user_input:
        return ("The annual fee structure varies:\n"
                "- BCA: ~₹1,50,000 per year\n"
                "- BBA: ₹1,11,000 - ₹1,25,000 per year\n"
                "- B.Com: ~₹80,000 per year\n"
                "- M.Sc: ~₹18,270 per year\n"
                "- MCA: ~₹1,17,000 (full course)\n"
                "Note: Approximate values. Contact admissions for exact details.")
    elif "student life" in user_input or "extracurriculars" in user_input or "clubs" in user_input:
        return ("Student life at KLESNC is vibrant:\n"
                "- Sports: Indoor/outdoor facilities + gym\n"
                "- Clubs: Literary club, NSS, NCC, Youth Red Cross\n"
                "- Events: Ignite, Colours Week, cultural/literary fests")
    elif "contact" in user_input or "address" in user_input or "location" in user_input:
        return ("Contact Details:\n"
                "KLE Society’s S. Nijalingappa College\n"
                "Address: #1040, II Block, Rajajinagar, Bengaluru – 560010\n"
                "Phone: +91-9141064927, +91-9513567755, 080-23526055 / 23325020\n"
                "Emails: info@klesnc.org, admissions@klesnc.org\n\n"
                "Landmarks:\n"
                "- 3 km from Yeshwanthpur Railway Station\n"
                "- 4 km from Bangalore City Railway Station / Majestic\n"
                "- 38 km from Kempegowda International Airport")
    elif "exit" in user_input or "quit" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "Sorry, I don't have that information. Please try something else or type 'help'."

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

    #Collect both fields (even if empty)
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
        #Always keep both columns in header
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "PU Marks", "UG Percentage/CGPA", "Mobile", "Course"])
        #Save both fields together
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
