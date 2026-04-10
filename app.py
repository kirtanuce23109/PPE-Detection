import streamlit as st
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# ---------------- HOME PAGE ----------------
def home():
    st.title("🚧 PPE Safety Monitoring System")

    st.header("🪖 What is PPE?")
    st.write("""
    PPE (Personal Protective Equipment) includes:
    - Helmet
    - Safety Vest
    - Gloves
    - Boots
    """)

    st.header("⚠️ Importance of PPE")
    st.write("""
    - Prevents injuries
    - Improves safety
    - Mandatory on construction sites
    """)

# ---------------- PROCESS VIDEO ----------------
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    workers = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True)

        for r in results:
            if r.boxes.id is None:
                continue

            for box, track_id, cls in zip(r.boxes.xyxy, r.boxes.id, r.boxes.cls):
                track_id = int(track_id)
                label = model.names[int(cls)]

                if track_id not in workers:
                    workers[track_id] = {"helmet": 0, "vest": 0}

                if "helmet" in label:
                    workers[track_id]["helmet"] += 1

                if "vest" in label:
                    workers[track_id]["vest"] += 1

    cap.release()
    return workers

# ---------------- CAMERA PAGE ----------------
def camera_page(video_path, title):
    st.title(title)

    uploaded_file = st.file_uploader("Upload Video", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)

    workers = process_video(video_path)

    total = len(workers)
    st.metric("👷 Total Workers", total)

    helmet_yes = sum(1 for w in workers.values() if w["helmet"] > 0)
    helmet_no = total - helmet_yes

    vest_yes = sum(1 for w in workers.values() if w["vest"] > 0)
    vest_no = total - vest_yes

    # Helmet Pie Chart
    fig1, ax1 = plt.subplots()
    ax1.pie([helmet_yes, helmet_no], labels=["Helmet", "No Helmet"], autopct='%1.1f%%')
    st.pyplot(fig1)

    # Vest Pie Chart
    fig2, ax2 = plt.subplots()
    ax2.pie([vest_yes, vest_no], labels=["Vest", "No Vest"], autopct='%1.1f%%')
    st.pyplot(fig2)

    # Worker details
    st.subheader("👷 Worker Details")
    for wid, w in workers.items():
        st.write(f"Worker {wid} → Helmet: {w['helmet']} | Vest: {w['vest']}")

# ---------------- NAVIGATION ----------------
page = st.sidebar.selectbox(
    "Select Page",
    ["Home", "Camera 1", "Camera 2", "Camera 3"]
)

if page == "Home":
    home()

elif page == "Camera 1":
    camera_page("cam1.mp4", "📷 Camera 1")

elif page == "Camera 2":
    camera_page("cam2.mp4", "📷 Camera 2")

elif page == "Camera 3":
    camera_page("cam3.mp4", "📷 Camera 3")
