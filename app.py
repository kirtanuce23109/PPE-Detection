import streamlit as st
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="PPE Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.title {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- VIDEO LINKS ----------------
cam1 = "https://drive.google.com/uc?id=1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "https://drive.google.com/uc?id=1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "https://drive.google.com/uc?id=11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- DATA ----------------
data = {
    "cam1": {"total": 12, "helmet_yes": 9, "helmet_no": 3, "vest_yes": 8, "vest_no": 4},
    "cam2": {"total": 10, "helmet_yes": 6, "helmet_no": 4, "vest_yes": 7, "vest_no": 3},
    "cam3": {"total": 8,  "helmet_yes": 5, "helmet_no": 3, "vest_yes": 4, "vest_no": 4},
}

# ---------------- VIDEO PLAYER ----------------
def show_video(url):
    st.markdown(f"""
    <video width="100%" controls>
      <source src="{url}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

# ---------------- CHART ----------------
def show_charts(d):
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.pie([d["helmet_yes"], d["helmet_no"]],
                labels=["Helmet", "No Helmet"],
                autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.pie([d["vest_yes"], d["vest_no"]],
                labels=["Vest", "No Vest"],
                autopct='%1.1f%%')
        st.pyplot(fig2)

# ---------------- HOME PAGE ----------------
def home():
    st.title("🚧 PPE Safety Dashboard")

    st.subheader("📡 Live Camera Feeds")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📷 Camera 1")
        show_video(cam1)

    with col2:
        st.markdown("### 📷 Camera 2")
        show_video(cam2)

    with col3:
        st.markdown("### 📷 Camera 3")
        show_video(cam3)

    st.markdown("---")

    st.info("👉 Use sidebar to view detailed analytics for each camera")

# ---------------- CAMERA PAGE ----------------
def camera_page(title, video_url, cam_key):
    st.title(title)

    show_video(video_url)

    d = data[cam_key]

    st.metric("👷 Total Workers", d["total"])

    show_charts(d)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "📷 Camera 1", "📷 Camera 2", "📷 Camera 3"]
)

# ---------------- ROUTING ----------------
if page == "🏠 Home":
    home()

elif page == "📷 Camera 1":
    camera_page("📷 Camera 1", cam1, "cam1")

elif page == "📷 Camera 2":
    camera_page("📷 Camera 2", cam2, "cam2")

elif page == "📷 Camera 3":
    camera_page("📷 Camera 3", cam3, "cam3")
