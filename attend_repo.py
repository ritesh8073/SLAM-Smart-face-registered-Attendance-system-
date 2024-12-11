import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Use the directory where app.py is located
folder_name = os.path.dirname(os.path.abspath(__file__))  # Directory where app.py is located

# Parse Attendance File
def parse_attendance(file_path):
    try:
        attendance_records = []
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            session_date = None
            present = []
            absent = []

            for line in lines:
                if line.startswith("--- Attendance Session:"):
                    if session_date:
                        attendance_records.append({"date": session_date, "present": present, "absent": absent})
                    timestamp = line.split(": ")[1].strip().split(" ")[0]
                    session_date = datetime.strptime(timestamp, "%Y-%m-%d")
                    present = []
                    absent = []
                elif line.startswith("Present Students:"):
                    present = [student.strip() for student in line.split(":")[1].split(",") if student.strip()]
                elif line.startswith("Absent Students:"):
                    absent = [student.strip() for student in line.split(":")[1].split(",") if student.strip()]

            # Add the last session's attendance
            if session_date:
                attendance_records.append({"date": session_date, "present": present, "absent": absent})

        return attendance_records

    except Exception as e:
        print(f"Error parsing attendance file: {e}")
        return []

# Calculate Attendance Percentages
def calculate_statistics(attendance_records):
    total_sessions = len(attendance_records)
    if total_sessions == 0:
        return {}

    attendance = {}
    for session in attendance_records:
        for student in session["present"]:
            attendance[student] = attendance.get(student, 0) + 1
        for student in session["absent"]:
            attendance.setdefault(student, 0)  # Ensure absent students are included

    stats = {student: (count / total_sessions) * 100 for student, count in attendance.items()}
    return stats

# Function to generate PDF
def generate_pdf(stats, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(220, height - 40, "Attendance Statistics")

    # Column Headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, "Above 75% Attendance")
    c.drawString(350, height - 80, "Below 75% Attendance")

    # Draw the lists of students
    c.setFont("Helvetica", 10)

    above_75 = [(student, percentage) for student, percentage in stats.items() if percentage >= 75]
    below_75 = [(student, percentage) for student, percentage in stats.items() if percentage < 75]

    y_position_above = height - 100
    y_position_below = height - 100

    # Printing Above 75% Attendance
    for student, percentage in above_75:
        c.drawString(50, y_position_above, f"{student}: {percentage:.2f}%")
        y_position_above -= 15
        if y_position_above < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position_above = height - 50

    # Printing Below 75% Attendance
    for student, percentage in below_75:
        c.drawString(350, y_position_below, f"{student}: {percentage:.2f}%")
        y_position_below -= 15
        if y_position_below < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position_below = height - 50

    c.save()

# Route to render the main page
@app.route('/')
def index():
    # Get all attendance files in the specified folder (filtering only .txt files)
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        files = [f for f in os.listdir(folder_name) if f.endswith('.txt')]  # Only .txt files
    else:
        files = []
    return render_template('attendance_statistics.html', files=files)

# Route to process the file and generate statistics
@app.route('/', methods=['POST'])
def process_file():
    selected_file = request.form.get('file')
    if selected_file:
        file_path = os.path.join(folder_name, selected_file)

        records = parse_attendance(file_path)
        if records:
            statistics = calculate_statistics(records)
            output_pdf = os.path.join(folder_name, f"attendance_report_{selected_file.split('.')[0]}.pdf")
            generate_pdf(statistics, output_pdf)

            return jsonify({
                'status': 'success',
                'file_name': f"attendance_report_{selected_file.split('.')[0]}.pdf"
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to parse attendance file.'})
    return jsonify({'status': 'error', 'message': 'No file selected.'})

# Route to download the PDF
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(folder_name, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
