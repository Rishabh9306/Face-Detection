import cv2
import mediapipe as mp
import os
from datetime import datetime
import calendar
from openpyxl import Workbook, load_workbook
import streamlit as st

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("😊 Good Morning! Have a Nice Day")
st.write("Enter your name and press Start Attendance")

# ---------------- EXCEL FILE ----------------
excel_file = "Attendance.xlsx"

if not os.path.exists(excel_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["Name", "Date", "Day", "Time"])
    wb.save(excel_file)

# ---------------- FACE DETECTION ----------------
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(0.5)

# ---------------- ATTENDANCE FUNCTION ----------------
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    day = calendar.day_name[now.weekday()]
    time = now.strftime("%H:%M:%S")

    wb = load_workbook(excel_file)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == name and row[1] == date:
            return False

    ws.append([name, date, day, time])
    wb.save(excel_file)
    return True

# ---------------- CAMERA FUNCTION ----------------
def start_camera(name):
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            st.error("Camera not accessible")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        stframe.image(frame, channels="BGR")

        if results.detections:
            saved = mark_attendance(name)
            if saved:
                st.success(f"✔ Attendance marked for {name}")
            else:
                st.warning(f"⚠ {name} already marked today")
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- STREAMLIT UI ----------------
name = st.text_input("Enter Your Name")

start = st.button("Start Attendance", key="attendance_btn")

if start:
    if name.strip() == "":
        st.warning("Please enter your name")
    else:
        start_camera(name)
        st.info("Next student can enter name 👇")
