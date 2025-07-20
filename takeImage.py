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
    if not enrollment_input and not name_input:
        st.warning("⚠️ Both Enrollment and Name are required.")
        return
    
    if not enrollment_input.isdigit():
        st.warning("⚠️ Enrollment must be a number.")
        return
    
    if not name_input.replace(" ", "").isalpha():
        st.warning("⚠️ Name must contain only alphabets.")
        return
    
    enrollment = int(enrollment_input)
    name = name_input.strip().title()
    matching_row, exists = student_exists(enrollment, studentdetail_path)
    
    if exists:
        st.warning("⚠️ This student is already registered.")
        st.subheader("📄 Student Record:")
        st.table(matching_row)
        return
    
    student_folder_path = os.path.join("TrainingImage", f"{enrollment}_{name}")
    os.makedirs(student_folder_path, exist_ok=True)

    try:
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcascade_path)
        sampleNum = 0
        text_to_speech("Please Face the camera")
                    
        while sampleNum < 50:
            ret, img = cam.read()
            if not ret:
                st.error("❌ Failed to access the camera.")
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
                        
            for (x, y, w, h) in faces:
                face_image = gray[y:y + h, x:x + w]
                file_path = os.path.join(student_folder_path, f"{name}_{enrollment}_{sampleNum}.jpg")
                cv2.imwrite(file_path, face_image)
                
                sampleNum += 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                            
            cv2.imshow("Capturing Images (Press 'q' to quit)", img)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
        cam.release()
        cv2.destroyAllWindows()
        
        if sampleNum == 0:
            os.rmdir(student_folder_path)
            st.warning("⚠️ No face detected. Please try again in proper lighting.")
            text_to_speech("No face detected. Please try again.")
            return

        # Save student details
        with open(studentdetail_path, "a+", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([enrollment, name])

        st.success(f"✅ Saved {sampleNum} images for {name} (Enrollment: {enrollment})")
        text_to_speech(f"Images saved for {name}, Roll Number {enrollment}.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        text_to_speech("An error occurred while taking images.")
