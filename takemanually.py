import streamlit as st
import pandas as pd
from datetime import datetime
import os

def manualAttendance(subject_input, enrollment_input, name_input, studentdetail_path, text_to_speech):
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
            
            attendance_df = pd.DataFrame([{
                    "Enrollment": enrollment,
                    "Name": name,
                    "Present": 1
                }])
            
            students_df = pd.read_csv(studentdetail_path)
            
            if students_df[(students_df["Enrollment"] == enrollment)].empty:
                st.error("🚫 Student not found in the official records.")
                text_to_speech("Please register yourself first")
                return
            
            # I would only do this if I weren't planning to display the entered details (attendance_df) to user
            # students_df[date] = students_df.apply(
            #                         lambda row: 1 if row["Enrollment"] == enrollment and row["Name"] == name else 0,
            #                         axis=1
            #                     )
        
            merged = pd.merge(students_df, attendance_df, on=["Enrollment", "Name"], how="left")
            merged[date] = merged.get(date, merged.get("Present", 0)).fillna(0)
            if "Present" in merged.columns:
                merged.drop(columns=["Present"], inplace=True)
            
            subject_folder = os.path.join("Attendance", subject)
            os.makedirs(subject_folder, exist_ok=True)
            
            attendance_csv = os.path.join(subject_folder, "attendance.csv")
            if os.path.exists(attendance_csv):
                existing_df = pd.read_csv(attendance_csv)
                final_df = pd.merge(existing_df, merged, on=["Enrollment", "Name", date], how="outer")
                final_df = final_df.drop_duplicates(subset=["Enrollment"], keep="last").reset_index(drop=True)
            else:
                final_df = merged
            
            attendance_cols = [col for col in final_df.columns if col not in ["Enrollment", "Name", "Attendance"]]
            # final_df = final_df.loc[:, ~final_df.columns.str.endswith(('_x', '_y'))]
            final_df[attendance_cols] = final_df[attendance_cols].fillna(0)
            final_df["Attendance"] = final_df[attendance_cols].mean(axis=1).apply(lambda x: f"{int(x * 100)}%")
            final_df.to_csv(attendance_csv, index=False)
            
            st.subheader("✅ Current Entries")
            st.dataframe(attendance_df)
            st.success(f"✔️ Added {name} - {enrollment}")
            text_to_speech(f"Attendance saved successfully for {subject}")
                    