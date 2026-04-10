import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="PPE Dashboard", layout="wide")

# ---------------- VIDEO LINKS ----------------
cam1 = "https://drive.google.com/uc?id=1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "https://drive.google.com/uc?id=1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "https://drive.google.com/uc?id=11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- REAL DATA (REPLACE WITH YOUR OUTPUT) ----------------
data = {
    "cam1": {"total": 12, "helmet_yes": 9, "helmet_no": 3, "vest_yes": 8, "vest_no": 4},
    "cam2": {"total": 10, "helmet_yes": 6, "helmet_no": 4, "vest_yes": 7, "vest_no": 3},
    "cam3": {"total": 8,  "helmet_yes": 5, "helmet_no": 3, "vest_yes": 4, "vest_no": 4},
}

# ---------------- CAMERA PAGE ----------------
def camera_page(title, video_url, cam_key):

    st.title(title)

    # FIXED VIDEO PLAYER
    st.markdown(f"""
    <video width="100%" controls>
      <source src="{video_url}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

    d = data[cam_key]

    st.metric("👷 Total Workers", d["total"])

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

# ---------------- NAV ----------------
page = st.sidebar.selectbox(
    "Select Page",
    ["Camera 1", "Camera 2", "Camera 3"]
)

if page == "Camera 1":
    camera_page("📷 Camera 1", cam1, "cam1")

elif page == "Camera 2":
    camera_page("📷 Camera 2", cam2, "cam2")

elif page == "Camera 3":
    camera_page("📷 Camera 3", cam3, "cam3")
