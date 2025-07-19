import pandas as pd
from glob import glob
import os
import streamlit as st
import csv

def selectSubject(subject_input, text_to_speech):
    if subject_input:
        if not subject_input.replace(" ", "").isalpha():
            st.warning("⚠️ Name must contain only alphabets.")
        else:
            subject = subject_input.strip().title()
            try:
                folder_path = os.path.join("Attendance", subject)
                if not os.path.exists(folder_path):
                    st.error("Subject folder does not exist.")
                    return

                filenames = glob(os.path.join(folder_path, f"{subject}*.csv"))
                if not filenames:
                    st.warning("No attendance files found for this subject.")
                    return

                df_list = [pd.read_csv(f) for f in filenames]
                newdf = df_list[0]

                for i in range(1, len(df_list)):
                    newdf = newdf.merge(df_list[i], how="outer")

                newdf.fillna(0, inplace=True)

                # Calculate attendance percentage
                attendance_cols = newdf.columns[2:]  # skipping Enrollment and Name
                newdf["Attendance"] = newdf[attendance_cols].mean(axis=1).apply(lambda x: f"{int(round(x * 100))}%")

                output_path = os.path.join(folder_path, "attendance.csv")
                newdf.to_csv(output_path, index=False)

                st.dataframe(newdf)

            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
                text_to_speech("Failed to display attendance.")
