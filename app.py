import streamlit as st
import matplotlib.pyplot as plt
import json

# ---------------- CONFIG ----------------
st.set_page_config(page_title="PPE Safety Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #0B0F1A; }

h1, h2, h3 { color: #FFD700; }

.warning {
    background-color: #ff4b4b;
    padding: 10px;
    border-radius: 10px;
    color: white;
}

.safe {
    background-color: #00c853;
    padding: 10px;
    border-radius: 10px;
    color: white;
}

.watermark {
    position: fixed;
    top: 10px;
    right: 20px;
    opacity: 0.6;
    font-size: 16px;
    color: #FFD700;
    z-index: 1000;
}
</style>

<div class="watermark">
👷 Kirtan Gajjar
</div>
""", unsafe_allow_html=True)

# ---------------- VIDEO FILE IDs ----------------
cam1 = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- LOAD REAL DATA ----------------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {"total": 0, "helmet_yes": 0, "helmet_no": 0, "vest_yes": 0, "vest_no": 0}

data = {
    "cam1": load_data("cam1_data.json"),
    "cam2": load_data("cam2_data.json"),
    "cam3": load_data("cam3_data.json"),
}

# ---------------- VIDEO PLAYER ----------------
def show_video(file_id):
    st.markdown(f"""
    <iframe src="https://drive.google.com/file/d/{file_id}/preview"
    width="100%" height="300" allow="autoplay"></iframe>
    """, unsafe_allow_html=True)

# ---------------- PIE CHART ----------------
def pie_chart(values, labels):
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    return fig

# ---------------- HOME PAGE ----------------
def home():
    st.title("🚧 PPE SAFETY DASHBOARD")

    total_workers = sum(d["total"] for d in data.values())
    total_helmet = sum(d["helmet_yes"] for d in data.values())
    total_vest = sum(d["vest_yes"] for d in data.values())

    col1, col2, col3 = st.columns(3)

    col1.metric("👷 Total Workers", total_workers)
    col2.metric("🪖 Helmet Compliance", f"{(total_helmet/total_workers)*100:.1f}%" if total_workers else "0%")
    col3.metric("🦺 Vest Compliance", f"{(total_vest/total_workers)*100:.1f}%" if total_workers else "0%")

    st.subheader("📊 Overall Safety Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(pie_chart([total_helmet, total_workers-total_helmet],
                            ["Helmet", "No Helmet"]))

    with col2:
        st.pyplot(pie_chart([total_vest, total_workers-total_vest],
                            ["Vest", "No Vest"]))

    st.subheader("📡 Live Camera Feeds")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📷 Camera 1")
        show_video(cam1)
        if st.button("View Camera 1"):
            st.session_state.page = "Camera 1"

    with col2:
        st.markdown("### 📷 Camera 2")
        show_video(cam2)
        if st.button("View Camera 2"):
            st.session_state.page = "Camera 2"

    with col3:
        st.markdown("### 📷 Camera 3")
        show_video(cam3)
        if st.button("View Camera 3"):
            st.session_state.page = "Camera 3"

# ---------------- CAMERA PAGE ----------------
def camera_page(title, cam_id, cam_key):
    st.title(title)

    show_video(cam_id)

    d = data[cam_key]

    st.metric("👷 Total Workers", d["total"])

    # SAFETY ALERT
    if d["helmet_no"] > 0:
        st.markdown('<div class="warning">⚠️ Some workers are NOT wearing helmets</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="safe">✅ All workers are safe</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    col1.pyplot(pie_chart([d["helmet_yes"], d["helmet_no"]],
                         ["Helmet", "No Helmet"]))

    col2.pyplot(pie_chart([d["vest_yes"], d["vest_no"]],
                         ["Vest", "No Vest"]))

    # ---------------- WORKER ESTIMATION ----------------
    st.subheader("👷 Worker Summary")

    st.write(f"✔ Workers with Helmet: {d['helmet_yes']}")
    st.write(f"❌ Workers without Helmet: {d['helmet_no']}")
    st.write(f"✔ Workers with Vest: {d['vest_yes']}")
    st.write(f"❌ Workers without Vest: {d['vest_no']}")

# ---------------- NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.sidebar.radio(
    "📊 Navigation",
    ["Home", "Camera 1", "Camera 2", "Camera 3"],
    index=["Home", "Camera 1", "Camera 2", "Camera 3"].index(st.session_state.page)
)

st.session_state.page = page

if page == "Home":
    home()
elif page == "Camera 1":
    camera_page("📷 Camera 1", cam1, "cam1")
elif page == "Camera 2":
    camera_page("📷 Camera 2", cam2, "cam2")
elif page == "Camera 3":
    camera_page("📷 Camera 3", cam3, "cam3")

# ---------------- FOOTER ----------------
st.markdown("""
<hr style="border:1px solid #333;">
<p style='text-align:center; color:gray; font-size:14px;'>
© 2026 PPE Safety Monitoring System | Developed by Kirtan Gajjar
</p>
""", unsafe_allow_html=True)
