import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
import streamlit as st
from PIL import ImageTk, Image


def TrainImage(haarcasecade_path, trainimagelabel_path, text_to_speech):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        faces, Id = getImagesAndLables("TrainingImage")
        
        if not faces or not Id:
            st.warning("⚠️ No face data found. Please register student images first.")
        else:
            recognizer.train(faces, np.array(Id))
            recognizer.save(trainimagelabel_path)

            st.success("✅ Image trained successfully")
            
    except Exception as e:
        st.error(f"❌ An error occurred while training: {str(e)}")


def getImagesAndLables(path):
    student_dirs = [os.path.join(path, d) for d in os.listdir(path)]
    imagePaths = [
        os.path.join(student_dirs[i], f)
        for i in range(len(student_dirs))
        for f in os.listdir(student_dirs[i])
    ]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
