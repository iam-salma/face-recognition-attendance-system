import pandas as pd
import os
import streamlit as st

def selectSubject(subject_input, studentdetail_path, text_to_speech):
    if subject_input:
        if not subject_input.replace(" ", "").isalpha():
            st.warning("⚠️ Name must contain only alphabets.")
        else:
            subject = subject_input.strip().title()
            folder_path = os.path.join("Attendance", subject)
            if not os.path.exists(folder_path):
                st.error("Subject folder does not exist.")
                return
            
            attendance_csv = os.path.join(folder_path, "attendance.csv")
            if os.path.exists(attendance_csv):
                df = pd.read_csv(attendance_csv)
                st.dataframe(df)
            else:
                st.error(f"Error occurred: {str(e)}")
                text_to_speech("Failed to display attendance.")
