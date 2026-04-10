import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="PPE Safety Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #0B0F1A; }

.metric-card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.warning {
    background: #ff4b4b;
    padding: 10px;
    border-radius: 10px;
    color: white;
}

.safe {
    background: #00c853;
    padding: 10px;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- VIDEO IDs ----------------
cam1 = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- DATA ----------------
data = {
    "cam1": {
        "total": 12,
        "helmet_yes": 9, "helmet_no": 3,
        "vest_yes": 8, "vest_no": 4,
        "workers": [
            {"id": 1, "helmet": True, "vest": True},
            {"id": 2, "helmet": False, "vest": True},
            {"id": 3, "helmet": True, "vest": False},
        ]
    },
    "cam2": {
        "total": 10,
        "helmet_yes": 6, "helmet_no": 4,
        "vest_yes": 7, "vest_no": 3,
        "workers": [
            {"id": 1, "helmet": True, "vest": True},
            {"id": 2, "helmet": False, "vest": False},
        ]
    },
    "cam3": {
        "total": 8,
        "helmet_yes": 5, "helmet_no": 3,
        "vest_yes": 4, "vest_no": 4,
        "workers": [
            {"id": 1, "helmet": True, "vest": False},
            {"id": 2, "helmet": False, "vest": True},
        ]
    }
}

# ---------------- VIDEO ----------------
def show_video(file_id):
    st.markdown(f"""
    <iframe src="https://drive.google.com/file/d/{file_id}/preview"
    width="100%" height="300"></iframe>
    """, unsafe_allow_html=True)

# ---------------- CHART ----------------
def pie_chart(values, labels):
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    return fig

# ---------------- HOME ----------------
def home():
    st.title("🚧 PPE SAFETY DASHBOARD")

    total_workers = sum(d["total"] for d in data.values())
    total_helmet = sum(d["helmet_yes"] for d in data.values())
    total_vest = sum(d["vest_yes"] for d in data.values())

    col1, col2, col3 = st.columns(3)

    col1.metric("👷 Total Workers", total_workers)
    col2.metric("🪖 Helmet Compliance", f"{(total_helmet/total_workers)*100:.1f}%")
    col3.metric("🦺 Vest Compliance", f"{(total_vest/total_workers)*100:.1f}%")

    st.subheader("📊 Overall Safety Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(pie_chart([total_helmet, total_workers-total_helmet],
                            ["Helmet", "No Helmet"]))

    with col2:
        st.pyplot(pie_chart([total_vest, total_workers-total_vest],
                            ["Vest", "No Vest"]))

    st.subheader("📡 Camera Feeds")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Camera 1")
        show_video(cam1)
        if st.button("View Camera 1"):
            st.session_state.page = "Camera 1"

    with col2:
        st.markdown("### Camera 2")
        show_video(cam2)
        if st.button("View Camera 2"):
            st.session_state.page = "Camera 2"

    with col3:
        st.markdown("### Camera 3")
        show_video(cam3)
        if st.button("View Camera 3"):
            st.session_state.page = "Camera 3"

# ---------------- CAMERA PAGE ----------------
def camera_page(title, cam_id, cam_key):
    st.title(title)

    show_video(cam_id)

    d = data[cam_key]

    st.metric("👷 Total Workers", d["total"])

    if d["helmet_no"] > 0:
        st.markdown('<div class="warning">⚠️ Helmet Missing</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="safe">✅ Safe</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    col1.pyplot(pie_chart([d["helmet_yes"], d["helmet_no"]],
                         ["Helmet", "No Helmet"]))

    col2.pyplot(pie_chart([d["vest_yes"], d["vest_no"]],
                         ["Vest", "No Vest"]))

    # -------- WORKER TABLE --------
    st.subheader("👷 Worker Details")

    for w in d["workers"]:
        helmet = "✅" if w["helmet"] else "❌"
        vest = "✅" if w["vest"] else "❌"
        st.write(f"Worker {w['id']} → Helmet: {helmet} | Vest: {vest}")

# ---------------- NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.sidebar.radio(
    "Navigation",
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
