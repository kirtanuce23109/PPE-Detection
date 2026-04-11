import streamlit as st
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="PPE Tracking Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #0B0F1A; color: white; }

.safe {
    background-color: #00c853;
    padding: 10px;
    border-radius: 10px;
    text-align:center;
}

.danger {
    background-color: #ff1744;
    padding: 10px;
    border-radius: 10px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD JSON ----------------
def load_workers(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

workers = load_workers("cam1_workers.json")

# ---------------- VIDEO ----------------
video_id = "1-lmVREDPnH03Qyo5tJ1pT4pioM8MsD_Q"

def show_video(file_id):
    st.markdown(f"""
    <iframe src="https://drive.google.com/file/d/{file_id}/preview"
    width="100%" height="350"></iframe>
    """, unsafe_allow_html=True)

# ---------------- CALCULATIONS ----------------
total_workers = len(workers)

helmet_yes = 0
vest_yes = 0

for w in workers.values():
    if w["helmet_time"] > w["no_helmet_time"]:
        helmet_yes += 1
    if w["vest_time"] > w["no_vest_time"]:
        vest_yes += 1

helmet_no = total_workers - helmet_yes
vest_no = total_workers - vest_yes

# ---------------- PIE FUNCTION ----------------
def pie_chart(values, labels):
    if sum(values) == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No Data", ha='center')
        ax.axis("off")
        return fig

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    return fig

# ---------------- UI ----------------
st.title("🚧 PPE WORKER TRACKING DASHBOARD")

# VIDEO
show_video(video_id)

# METRICS
col1, col2, col3 = st.columns(3)

col1.metric("👷 Total Workers", total_workers)

helmet_percent = (helmet_yes / total_workers * 100) if total_workers else 0
vest_percent = (vest_yes / total_workers * 100) if total_workers else 0

col2.metric("🪖 Helmet Compliance", f"{helmet_percent:.1f}%")
col3.metric("🦺 Vest Compliance", f"{vest_percent:.1f}%")

# SAFETY ALERT
if helmet_no > 0 or vest_no > 0:
    st.markdown('<div class="danger">⚠️ Unsafe Workers Detected</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="safe">✅ All Workers Safe</div>', unsafe_allow_html=True)

# CHARTS
c1, c2 = st.columns(2)

c1.pyplot(pie_chart([helmet_yes, helmet_no], ["Helmet", "No Helmet"]))
c2.pyplot(pie_chart([vest_yes, vest_no], ["Vest", "No Vest"]))

# ---------------- WORKER TABLE ----------------
st.subheader("👷 Worker-wise Tracking (Time Based)")

for wid, w in workers.items():

    helmet_status = "✅" if w["helmet_time"] > w["no_helmet_time"] else "❌"
    vest_status = "✅" if w["vest_time"] > w["no_vest_time"] else "❌"

    st.markdown(f"""
    **Worker {wid}**
    - 🪖 Helmet Time: {w['helmet_time']:.2f} sec
    - ❌ No Helmet Time: {w['no_helmet_time']:.2f} sec
    - 🦺 Vest Time: {w['vest_time']:.2f} sec
    - ❌ No Vest Time: {w['no_vest_time']:.2f} sec
    - Status: Helmet {helmet_status} | Vest {vest_status}
    """)
