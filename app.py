import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="PPE Dashboard", layout="wide")

# ---------------- GOOGLE DRIVE LINKS ----------------
cam1 = "https://drive.google.com/uc?id=1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "https://drive.google.com/uc?id=1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "https://drive.google.com/uc?id=11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- HOME ----------------
def home():
    st.title("🚧 PPE Safety Monitoring System")

    st.markdown("""
    ### 🪖 PPE Importance
    - Helmet and vest are mandatory
    - Reduces accidents
    - Improves safety compliance
    """)

# ---------------- CAMERA PAGE ----------------
def camera_page(title, video_url):

    st.title(title)

    # Show video from Google Drive
    st.video(video_url)

    # Sample data (you can upgrade later)
    total_workers = 12
    helmet_yes = 9
    helmet_no = 3
    vest_yes = 8
    vest_no = 4

    st.metric("👷 Total Workers", total_workers)

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.pie([helmet_yes, helmet_no],
                labels=["Helmet", "No Helmet"],
                autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.pie([vest_yes, vest_no],
                labels=["Vest", "No Vest"],
                autopct='%1.1f%%')
        st.pyplot(fig2)

    st.subheader("👷 Worker Details")

    for i in range(1, total_workers + 1):
        st.write(f"Worker {i} → Helmet: ✅ | Vest: ❌")

# ---------------- NAVIGATION ----------------
page = st.sidebar.selectbox(
    "📌 Select Page",
    ["Home", "Camera 1", "Camera 2", "Camera 3"]
)

if page == "Home":
    home()

elif page == "Camera 1":
    camera_page("📷 Camera 1", cam1)

elif page == "Camera 2":
    camera_page("📷 Camera 2", cam2)

elif page == "Camera 3":
    camera_page("📷 Camera 3", cam3)
