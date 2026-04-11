import streamlit as st
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="PPE AI Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #0B0F1A; }

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
</style>
""", unsafe_allow_html=True)

# ---------------- VIDEO IDS ----------------
cam1 = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2 = "1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3 = "11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

# ---------------- LOAD WORKER DATA ----------------
def load_workers(file):
    with open(file, "r") as f:
        return json.load(f)

workers_data = {
    "cam1": load_workers("cam1_workers.json"),
    "cam2": load_workers("cam2_workers.json"),
    "cam3": load_workers("cam3_workers.json"),
}

# ---------------- VIDEO ----------------
def show_video(file_id):
    st.markdown(f"""
    <iframe src="https://drive.google.com/file/d/{file_id}/preview"
    width="100%" height="300"></iframe>
    """, unsafe_allow_html=True)

# ---------------- CAMERA PAGE ----------------
def camera_page(title, cam_id, cam_key):

    st.title(title)
    show_video(cam_id)

    workers = workers_data[cam_key]

    st.metric("👷 Total Workers", len(workers))

    # -------- SAFETY CHECK --------
    unsafe = sum(1 for w in workers.values() if w["no_helmet_time"] > 1)

    if unsafe > 0:
        st.markdown('<div class="warning">⚠️ Unsafe workers detected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="safe">✅ All workers safe</div>', unsafe_allow_html=True)

    # -------- PIE CHART --------
    helmet_yes = sum(1 for w in workers.values() if w["helmet_time"] > w["no_helmet_time"])
    helmet_no = len(workers) - helmet_yes

    vest_yes = sum(1 for w in workers.values() if w["vest_time"] > w["no_vest_time"])
    vest_no = len(workers) - vest_yes

    col1, col2 = st.columns(2)

    fig1, ax1 = plt.subplots()
    ax1.pie([helmet_yes, helmet_no], labels=["Helmet", "No Helmet"], autopct='%1.1f%%')
    col1.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.pie([vest_yes, vest_no], labels=["Vest", "No Vest"], autopct='%1.1f%%')
    col2.pyplot(fig2)

    # -------- WORKER TABLE --------
    st.subheader("👷 Worker Tracking (Time-Based)")

    for wid, w in workers.items():

        helmet_status = "✅" if w["helmet_time"] > w["no_helmet_time"] else "❌"
        vest_status = "✅" if w["vest_time"] > w["no_vest_time"] else "❌"

        st.markdown(f"""
        **Worker {wid}**
        - 🪖 Helmet Time: {w['helmet_time']:.1f}s
        - ❌ No Helmet Time: {w['no_helmet_time']:.1f}s
        - 🦺 Vest Time: {w['vest_time']:.1f}s
        - ❌ No Vest Time: {w['no_vest_time']:.1f}s
        - Status: Helmet {helmet_status} | Vest {vest_status}
        """)

# ---------------- NAV ----------------
page = st.sidebar.radio(
    "Navigation",
    ["Camera 1", "Camera 2", "Camera 3"]
)

if page == "Camera 1":
    camera_page("📷 Camera 1", cam1, "cam1")

elif page == "Camera 2":
    camera_page("📷 Camera 2", cam2, "cam2")

elif page == "Camera 3":
    camera_page("📷 Camera 3", cam3, "cam3")
