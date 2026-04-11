import streamlit as st
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="PPE Dashboard", layout="wide")

# ------------------ STYLE ------------------
st.markdown("""
<style>
body { background-color: #0B0F1A; color: white; }

.card {
    padding: 20px;
    border-radius: 15px;
    background: #111827;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
    text-align: center;
}

.safe { background-color: #00c853; padding:10px; border-radius:10px; }
.danger { background-color: #ff1744; padding:10px; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD JSON ------------------
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {"total":0,"helmet_yes":0,"helmet_no":0,"vest_yes":0,"vest_no":0}

cam_data = {
    "Camera 1": load_data("cam1_data.json"),
    "Camera 2": load_data("cam2_data.json"),
    "Camera 3": load_data("cam3_data.json"),
}

# ------------------ VIDEO ------------------
def show_video(file_id):
    st.markdown(f"""
    <iframe src="https://drive.google.com/file/d/{file_id}/preview"
    width="100%" height="300" allow="autoplay"></iframe>
    """, unsafe_allow_html=True)

# ------------------ PIE CHART ------------------
def pie_chart(values, labels):
    if sum(values) == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No Data", ha='center')
        ax.axis("off")
        return fig

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    return fig

# ------------------ CAMERA PAGE ------------------
def camera_page(name, data, video_id):

    st.title(f"📷 {name}")
    show_video(video_id)

    st.subheader("👷 Workers Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Workers", data["total"])
    col2.metric("Helmet %", f"{(data['helmet_yes']/(data['total']+1))*100:.1f}")
    col3.metric("Vest %", f"{(data['vest_yes']/(data['total']+1))*100:.1f}")

    # SAFETY ALERT
    if data["helmet_no"] > 0 or data["vest_no"] > 0:
        st.markdown('<div class="danger">⚠️ Unsafe Workers Detected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="safe">✅ All Workers Safe</div>', unsafe_allow_html=True)

    # PIE CHARTS
    c1, c2 = st.columns(2)

    c1.pyplot(pie_chart(
        [data["helmet_yes"], data["helmet_no"]],
        ["Helmet", "No Helmet"]
    ))

    c2.pyplot(pie_chart(
        [data["vest_yes"], data["vest_no"]],
        ["Vest", "No Vest"]
    ))

# ------------------ HOME PAGE ------------------
def home_page():

    st.title("🚧 PPE SAFETY DASHBOARD")

    total = sum(d["total"] for d in cam_data.values())
    helmet = sum(d["helmet_yes"] for d in cam_data.values())
    vest = sum(d["vest_yes"] for d in cam_data.values())

    col1, col2, col3 = st.columns(3)

    col1.metric("👷 Total Workers", total)
    col2.metric("🪖 Helmet Compliance", f"{(helmet/(total+1))*100:.1f}%")
    col3.metric("🦺 Vest Compliance", f"{(vest/(total+1))*100:.1f}%")

    st.markdown("---")
    st.subheader("🎥 Live Camera Overview")

    cam1 = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
    cam2 = "1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
    cam3 = "11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

    c1, c2, c3 = st.columns(3)

    with c1:
        st.write("Camera 1")
        show_video(cam1)
        st.markdown("[➡ View Details](#camera-1)")

    with c2:
        st.write("Camera 2")
        show_video(cam2)
        st.markdown("[➡ View Details](#camera-2)")

    with c3:
        st.write("Camera 3")
        show_video(cam3)
        st.markdown("[➡ View Details](#camera-3)")

# ------------------ NAVIGATION ------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Camera 1", "Camera 2", "Camera 3"]
)

cam1_id = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"
cam2_id = "1K3JgrAP4ez33oDYy6gromZrIg52NCDx9"
cam3_id = "11WwV3JBL6oowDhY9fMN63OXKsJ93GoqS"

if page == "Home":
    home_page()

elif page == "Camera 1":
    camera_page("Camera 1", cam_data["Camera 1"], cam1_id)

elif page == "Camera 2":
    camera_page("Camera 2", cam_data["Camera 2"], cam2_id)

elif page == "Camera 3":
    camera_page("Camera 3", cam_data["Camera 3"], cam3_id)
