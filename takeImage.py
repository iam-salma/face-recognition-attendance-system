import cv2
import csv
import os
import streamlit as st
import pandas as pd

def student_exists(enrollment, studentdetail_path):
    df = pd.read_csv(studentdetail_path)
    matching_row = df[df["Enrollment"] == enrollment]
    return [matching_row, not matching_row.empty]

def TakeImage(enrollment_input, name_input, haarcascade_path, studentdetail_path, text_to_speech):
    if enrollment_input and name_input:
        if not enrollment_input.isdigit():
            st.warning("⚠️ Enrollment must be a number.")
        elif not name_input.replace(" ", "").isalpha():
            st.warning("⚠️ Name must contain only alphabets.")
        else:
            enrollment = int(enrollment_input)
            name = name_input.strip().title()
            matching_row, exists = student_exists(enrollment, studentdetail_path)
            if exists:
                st.warning("⚠️ This student is already registered.")
                st.subheader("📄 Student Record:")
                st.table(matching_row)
            else:
                student_folder_path = os.path.join("TrainingImage", f"{enrollment}_{name}")
                os.makedirs(student_folder_path, exist_ok=True)

                try:
                    cam = cv2.VideoCapture(0)
                    detector = cv2.CascadeClassifier(haarcascade_path)
                    
                    sampleNum = 0
                    text_to_speech("Please Face the camera")
                    
                    while True:
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.3, 5)
                        
                        for (x, y, w, h) in faces:
                            sampleNum += 1
                            file_path = os.path.join(student_folder_path, f"{name}_{enrollment}_{sampleNum}.jpg")
                            cv2.imwrite(file_path, gray[y:y + h, x:x + w])
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            cv2.putText(img, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                            
                        cv2.imshow("Capturing Images (Press 'q' to quit)", img)
                        
                        if cv2.waitKey(1) & 0xFF == ord("q") or sampleNum >= 50:
                            break
                        
                    cam.release()
                    cv2.destroyAllWindows()
                    
                    if sampleNum == 0:
                        os.rmdir(student_folder_path)
                        st.warning("⚠️ No face detected. Please try again in proper lighting.")
                        text_to_speech("No face detected. Please try again.")
                        return
                    
                    with open(studentdetail_path, "a+", newline="") as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow([enrollment, name])
                    
                    st.success(f"✅ Images have been successfully saved for {name}, Roll Number {enrollment}.")
                    text_to_speech(f"Images have been successfully saved for {name}, Roll Number {enrollment}.")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred while taking images: {str(e)}")
