import streamlit as st
import os
import cv2
import csv
import pandas as pd
import numpy as np
import datetime
import time
import pyttsx3
from PIL import Image

from takeImage import TakeImage
from trainImage import TrainImage
from Attendance import chooseSubject
from takemanually import manualAttendance
from view_attendance import selectSubject
from delete import deleteEntry


haarcasecade_path = "haarcascades/haarcascade_frontalface_alt.xml"
trainimagelabel_path = "TrainingImageLabel/trainer.yaml"
studentdetail_path = "StudentDetails/studentdetails.csv"

os.makedirs("TrainingImageLabel", exist_ok=True)
os.makedirs("TrainingImage", exist_ok=True)
os.makedirs("Attendance", exist_ok=True)
os.makedirs("StudentDetails", exist_ok=True)


if not os.path.exists(trainimagelabel_path):
    with open(trainimagelabel_path, "w", newline="") as f:
        pass
    
if not os.path.exists(studentdetail_path):
    with open(studentdetail_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Enrollment", "Name"])
        csvfile.flush()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


st.sidebar.title("Smart College Attendance")
menu = st.sidebar.radio("Navigate", ["Home", "Register Student", "Take Attendance", "Manual Attendance", "View Attendance", "Delete Student"],
                        key="main_menu")

st.title("Face Recognition Based Attendance System")

if menu == "Home":
    col1, col2 = st.columns([1, 4], gap="medium")
    with col1:
        st.image("UI_Image/0003.png", width=120)
    with col2:
        st.markdown("#### An AI-Powered Attendance System")
    st.markdown("---")
    st.markdown(
        """
        Welcome! This system uses facial recognition to streamline the attendance process.
        
        ### Key Features:
        - **📝 Register Student Faces:** Easily capture and store student images.
        - **🧠 Train Recognition Model:** Train the AI with the registered data.
        - **📸 Real-time Attendance:** Use a webcam for automatic attendance.
        - **📝 Manual Attendance:** Add Attendance manually.
        - **📊 View Attendance Logs:** Access and review detailed attendance records.
        - **❌ Delete Registered students:** delete student records.
        """
    )

elif menu == "Register Student":
    st.header("👤Register a New Student")
    enrollment_input = st.text_input("Enrollment No")
    name_input = st.text_input("Name")

    if st.button("Take Image"):
        TakeImage(
            enrollment_input,
            name_input,
            haarcasecade_path,
            studentdetail_path,
            text_to_speech,
            )
                        
    if st.button("Train Image"):
        TrainImage(
            haarcasecade_path,
            trainimagelabel_path,
            text_to_speech
            )


elif menu == "Take Attendance":
    st.subheader("📸 Fill Attendance")
    subject_input = st.text_input("Enter Subject")
    
    if st.button("Start Attendance", key="start_attendance"):
        chooseSubject(
            subject_input,
            haarcasecade_path,
            trainimagelabel_path,
            studentdetail_path,
            text_to_speech
            )

elif menu == "Manual Attendance":
    st.subheader("📋 Manual Attendance Entry")
    subject_input = st.text_input("Enter Subject")
    enrollment_input = st.text_input("Enrollment No")
    name_input = st.text_input("Name")
    
    if st.button("Add Attendance", key="manual_attendance"):
        manualAttendance(
            subject_input,
            enrollment_input,
            name_input,
            studentdetail_path,
            text_to_speech)

elif menu == "View Attendance":
    st.subheader("Attendance Records")
    subject_input = st.text_input("Enter Subject", key="view_attendance")

    if st.button("View Attendance", key="view_attendance_btn"):
        selectSubject(
            subject_input,
            studentdetail_path,
            text_to_speech
            )

elif menu == "Delete Student":
    st.header("🗑️ Delete a Registered Student")
    enrollment_input = st.text_input("Enter Enrollment No to delete")
    
    if st.button("Delete Permanantly"):
        deleteEntry(
            enrollment_input,
            haarcasecade_path,
            trainimagelabel_path,
            studentdetail_path,
            text_to_speech
            )
