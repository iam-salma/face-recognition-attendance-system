<p align="center">
  <img width="200" height="200" alt="ChatGPT Image Jul 20, 2025, 06_13_39 AM" src="https://github.com/user-attachments/assets/a9397cd9-d3ab-4925-aadc-c42f51115fdc" />
</p>

<h1 align="center">
  Face Recognition Based Attendance System
</h1>

<p align="center">
  <a href="https://github.com/iam-salma/face-recognition-attendance-system/stargazers">
    <img src="https://img.shields.io/github/stars/iam-salma/face-recognition-attendance-system?style=social" alt="Stars"/>
  </a>
  <a href="https://github.com/iam-salma/face-recognition-attendance-system/fork">
    <img src="https://img.shields.io/github/forks/iam-salma/face-recognition-attendance-system?style=social" alt="Forks"/>
  </a>
  <a href="https://github.com/iam-salma/face-recognition-attendance-system/issues">
    <img src="https://img.shields.io/github/issues/iam-salma/face-recognition-attendance-system" alt="Issues"/>
  </a>
  <a href="https://github.com/iam-salma/face-recognition-attendance-system/pulls">
    <img src="https://img.shields.io/github/issues-pr/iam-salma/face-recognition-attendance-system" alt="Pull Requests"/>
  </a>
  <img src="https://img.shields.io/github/last-commit/iam-salma/face-recognition-attendance-system" alt="Last Commit"/>
</p>

A real-time face recognition-based attendance system built using **Streamlit** for the user interface, **OpenCV** for face detection and recognition, and **Haar Cascade classifiers** for facial feature extraction. This system allows you to register students, train a face recognition model, and take or view attendance with ease.

---

## 🚀 Features

- 🧑‍🎓 Register students with facial image capture
- 🧠 Train model using OpenCV and Haar Cascades
- 🤖 Automatic attendance using webcam and face recognition
- ✍️ Manual attendance entry
- 📅 View attendance records by subject and date + percentage
- 🗑️ Delete student data from the system
- 🔈 Text-to-speech for better accessibility

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** – GUI and user interactions
- **OpenCV** – Image processing and recognition
- **Haar Cascades** – Face detection
- **CSV** – Storage of student details and attendance logs

---

## 📁 Project Structure

```
📦face-recognition-attendance/
├── app.py                         # Main Streamlit app
├── takeImage.py                   # Capture and save student face
├── trainImage.py                  # Train recognition model
├── automaticAttendance.py         # Detect and mark attendance
├── takemanually.py                # Manual attendance input
├── view_attendance.py             # Display attendance by subject/date
├── delete.py                      # Delete student and retrain
├── db.py                          # CSV-based student DB utilities
├── TrainingImage/                 # Folder storing face images
├── TrainingImageLabel/            # Trained model file (e.g., .yml)
├── StudentDetails/                # CSV file for student info
├── Attendance/                    # Attendance records
├── HaarCascade/haarcascade_frontalface_default.xml
```

---

## ▶️ How to Run

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the app**
```bash
streamlit run app.py
```

3. **Use Interface**
- Register students
- Train model
- Take automatic or manual attendance
- View or delete records

---

## ✅ Requirements

- Webcam-enabled system
- Python 3.8 or higher

---

## 📌 Notes

- Make sure the `haarcascade_frontalface_default.xml` file is available in the correct path.
- After deleting a student, the model is retrained automatically.
- CSV files are used for storage – you can upgrade to a database like PostgreSQL if needed.

---

If you found this project helpful or interesting, please consider giving it a ⭐️ on GitHub — it motivates and helps others discover it! ✌️

ENJOY! 🎉
