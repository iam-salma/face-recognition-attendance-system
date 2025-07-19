import streamlit as st
import pandas as pd
import shutil
import os
from trainImage import TrainImage

def student_exists(enrollment, studentdetail_path):
    df = pd.read_csv(studentdetail_path)
    matching_row = df[df["Enrollment"] == enrollment]
    return [matching_row, not matching_row.empty]

def deleteEntry(enrollment_input, studentdetail_path, text_to_speech):
    if enrollment_input:
        if not enrollment_input.isdigit():
            st.warning("⚠️ Enrollment must be a number.")
        else:
            enrollment = int(enrollment_input)
            matching_row, exists = student_exists(enrollment, studentdetail_path)
            if exists:
                st.subheader("📄 Student Record:")
                st.table(matching_row)
                try:
                    enrollment = int(matching_row["Enrollment"].values[0])
                    name = matching_row["Name"].values[0]

                    df = pd.read_csv(studentdetail_path, header=None, names=["Enrollment", "Name"])
                    df = df[df["Enrollment"] != enrollment]  # Remove the row
                    df.to_csv(studentdetail_path, header=False, index=False)

                    student_folder = os.path.join("TrainingImage", f"{enrollment}_{name}")
                    shutil.rmtree(student_path)
                    
                    TrainImage(
                        haarcasecade_path,
                        trainimagelabel_path,
                        text_to_speech,
                    )

                    text_to_speech(f"Deleted student {name} successfully")
                    st.success(f"✅ Deleted student {name} ({enrollment}) successfully.")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred while deleting: {str(e)}")
            else:
                st.warning("⚠️ Student not found in records.")