import streamlit as st
import pandas as pd
from datetime import datetime
import os

def manualAttendance(subject_input, enrollment_input, name_input, text_to_speech):
    if subject_input and enrollment_input and name_input:
        if not subject_input.replace(" ", "").isalpha():
            st.warning("⚠️ Subject name must contain only alphabets.")
        if not enrollment_input.isdigit():
            st.warning("⚠️ Enrollment must be a number.")
        elif not name_input.replace(" ", "").isalpha():
            st.warning("⚠️ Name must contain only alphabets.")
        else:
            subject = subject_input.strip().title()
            enrollment = int(enrollment_input)
            name = name_input.strip().title()
            
            date = datetime.now().strftime("%Y-%m-%d")
            timeStamp = datetime.now().strftime("%H-%M-%S")
            st.subheader("✅ Current Entries")
            df = pd.DataFrame([{
                    "Enrollment": enrollment,
                    "Name": name,
                    date: 1
                }])
            st.dataframe(df)
                        
            subject_folder = os.path.join("Attendance", subject)
            os.makedirs(subject_folder, exist_ok=True)
            csv_path = os.path.join(subject_folder, f"{subject}_{date}_{timeStamp}.csv")
            df.to_csv(csv_path, index=False)
            st.success(f"✔️ Added {name} - {enrollment}")
            text_to_speech(f"Attendance saved successfully for {subject}")
                    