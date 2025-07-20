import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime
import time
import pyttsx3


def chooseSubject(subject_input, haarcasecade_path, trainimagelabel_path, studentdetail_path, text_to_speech):
    if subject_input:
        if not subject_input.replace(" ", "").isalpha():
            st.warning("⚠️ Subject Name must contain only alphabets.")
        else:
            subject = subject_input.strip().title()
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(trainimagelabel_path)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_DUPLEX
                
                students_df = pd.read_csv(studentdetail_path)
                attendance_df = pd.DataFrame(columns=["Enrollment", "Name"])
                end_time = time.time() + 5
                
                while time.time() < end_time:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    
                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 70:
                            student_row = students_df[students_df["Enrollment"] == Id]
                            if not student_row.empty:
                                name = student_row["Name"].values[0]
                                attendance_df.loc[len(attendance_df)] = [Id, name]
                                label = f"{Id}-{name}"
                                color = (0, 255, 0)
                            else:
                                label = "Unregistered"
                                color = (0, 165, 255)
                        else:
                            label = "Unknown"
                            color = (0, 0, 255)
                            
                        cv2.rectangle(im, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(im, label, (x, y - 10), font, 0.8, (255, 255, 255), 2)

                    cv2.imshow("Filling Attendance", im)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                cam.release()
                cv2.destroyAllWindows()
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
                text_to_speech("failed recognizing face please try again")
                cam.release()
                cv2.destroyAllWindows()
                return

            if attendance_df.empty:
                st.error("❌ failed recognizing face")
                text_to_speech("failed recognizing face please try again")
                return
            else:
                attendance_df = attendance_df.drop_duplicates(subset="Enrollment", keep="last").reset_index(drop=True)
                attendance_df["Present"] = 1
                date = datetime.now().strftime("%Y-%m-%d")
                
                merged = pd.merge(students_df, attendance_df, on=["Enrollment", "Name"], how="left")
                merged[date] = merged.get(date, merged.get("Present", 0)).fillna(0)
                if "Present" in merged.columns:
                    merged.drop(columns=["Present"], inplace=True)
                
                subject_folder = os.path.join("Attendance", subject)
                os.makedirs(subject_folder, exist_ok=True)
                
                attendance_csv = os.path.join(subject_folder, "attendance.csv")
                if os.path.exists(attendance_csv):
                    existing_df = pd.read_csv(attendance_csv)
                    final_df = pd.merge(existing_df, merged, on=["Enrollment", "Name"], how="outer")
                else:
                    final_df = merged
                    
                attendance_cols = final_df.columns[2:]  # Skip Enrollment and Name
                final_df[attendance_cols] = final_df[attendance_cols].fillna(0)
                final_df["Attendance"] = final_df[attendance_cols].mean(axis=1).apply(lambda x: f"{int(x * 100)}%")
                final_df.to_csv(attendance_csv, index=False)
                
                st.dataframe(attendance_df)
                st.success(f"✅ Attendance Filled Successfully for {subject}")
                text_to_speech(f"Attendance filled successfully for {subject}")
                
