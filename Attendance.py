import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
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
                df = pd.read_csv(studentdetail_path)
                
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_DUPLEX
                
                attendance = pd.DataFrame(columns=["Enrollment", "Name"])
                end_time = time.time() + 5

                while time.time() < end_time:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    
                    for (x, y, w, h) in faces:
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        
                        if conf < 70:
                            name = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                            attendance.loc[len(attendance)] = [Id, name]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(im, f"{Id}-{name}", (x, y - 10), font, 0.8, (255, 255, 255), 2)
                            
                        else:
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            cv2.putText(im, "Unknown", (x, y - 10), font, 0.8, (0, 0, 255), 2)

                    cv2.imshow("Filling Attendance", im)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                cam.release()
                cv2.destroyAllWindows()

                attendance.drop_duplicates(["Enrollment"], inplace=True)
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.now().strftime("%H-%M-%S")
                attendance[date] = 1

                subject_folder = os.path.join("Attendance", subject)
                os.makedirs(subject_folder, exist_ok=True)
                file_path = os.path.join(subject_folder, f"{subject}_{date}_{timeStamp}.csv")
                attendance.to_csv(file_path, index=False)

                st.dataframe(attendance)
                st.success(f"✅ Attendance Filled Successfully for {subject}")
                text_to_speech(f"Attendance filled successfully for {subject}")
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
                text_to_speech("No face found for attendance")
                cam.release()
                cv2.destroyAllWindows()
