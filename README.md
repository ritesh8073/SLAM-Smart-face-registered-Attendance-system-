# Attendance System using Face Recognition

This project is an Attendance System that utilizes face recognition to mark attendance automatically. It is designed to enhance efficiency and accuracy in tracking student or employee attendance.

## Features
- Face recognition-based attendance marking
- Secure authentication system
- Manual attendance entry as a backup
- Attendance reports and analytics
- User-friendly interface
- Real-time data storage

## Technologies Used
- Python (OpenCV, NumPy, dlib, face_recognition library)
- Flask for the backend
- HTML, CSS, and JavaScript for the frontend
- SQLite or MySQL for database management

## Setup Instructions
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python libraries (install using `requirements.txt`)
- A webcam or external camera

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/PannagaJA/Attendance-System-using-face-recognition.git
   cd Attendance-System-using-face-recognition
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
![image](https://github.com/user-attachments/assets/dcd86f5a-6f6a-4dd5-9154-718b531fd4c1)
![image (1)](https://github.com/user-attachments/assets/5eace8bb-4410-4cd1-ab46-46f50953560c)
![image (2)](https://github.com/user-attachments/assets/65e0e812-c9ea-4c76-bd26-087d59acd4aa)
![image (3)](https://github.com/user-attachments/assets/6ebdb91c-9160-4921-9b91-8a8ec3589092)

   ```
4. Open your browser and navigate to `http://127.0.0.1:5000/`.

## How It Works
1. The system captures and stores face images of students/employees.
2. During attendance marking, the system compares live camera feeds with stored face data.
3. If a match is found, attendance is recorded automatically.
4. Attendance records can be viewed and exported.
5. 

## Customization
- Modify `app.py` to add new functionalities.
- Update `templates/` to change UI elements.
- Adjust face recognition parameters in `face_recognition.py`.

## Future Enhancements
- Integration with a college management system
- Cloud-based attendance storage
- AI-based analytics for attendance patterns

## License
This project is open-source and available for modification and distribution.

## Author
Ritesh N

