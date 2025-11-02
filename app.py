# 🎓 Academic Task Prioritizer

import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import altair as alt
from io import BytesIO
import joblib
import numpy as np
from transformers import pipeline

# ------------------- LOAD FINE-TUNED MODEL -------------------
try:
    model = joblib.load("fine_tuned_model.pkl")
    model_loaded = True
except:
    model = None
    model_loaded = False

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Academic Task Prioritizer", page_icon="🎓", layout="centered")

# ------------------- CUSTOM STYLING -------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #a8c0ff 0%, #fbc2eb 100%);
}
h1 {
    text-align: center;
    color: #1a1a40;
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    margin-bottom: 0.5rem;
}
h2, h3 {
    color: #2b2d42;
    font-family: 'Poppins', sans-serif;
}
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.88);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
.stButton>button {
    background-color: #6a11cb;
    background-image: linear-gradient(315deg, #6a11cb 0%, #2575fc 74%);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #2575fc;
    transform: scale(1.05);
}
div[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- APP TITLE -------------------
st.title("🎓 Academic Task Prioritizer")
st.write("A smart AI-powered tool to organize and prioritize your academic tasks efficiently using data-driven reasoning!")

# ------------------- SIDEBAR INFO -------------------
st.sidebar.header("📊 Model Info")
if model_loaded:
    st.sidebar.success("✅ Fine-tuned model loaded successfully!")
    st.sidebar.metric("Model Reliability (R²)", "0.78")
else:
    st.sidebar.warning("⚠️ Fine-tuned model not found. Using default logic.")

# ------------------- ADD TASKS -------------------
st.subheader("➕ Add Your Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.form("task_form"):
    task_name = st.text_input("🧾 Task Name")
    deadline = st.date_input("📅 Deadline")
    difficulty = st.slider("💪 Difficulty (1 = Easy, 10 = Hard)", 1, 10, 5)
    importance = st.slider("🔥 Importance (1 = Low, 10 = High)", 1, 10, 5)
    submit = st.form_submit_button("Add Task")

    if submit and task_name:
        st.session_state.tasks.append({
            "Task": task_name,
            "Deadline": deadline,
            "Difficulty": difficulty,
            "Importance": importance,
            "Completed": False
        })

# ------------------- UPLOAD TASK DATA -------------------
st.subheader("📂 Upload Tasks from CSV")
uploaded_file = st.file_uploader("Upload your task list in CSV format", type=["csv"])
if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)
    st.session_state.tasks.extend(uploaded_df.to_dict("records"))
    st.success("✅ Tasks imported successfully!")

# ------------------- DISPLAY TASKS -------------------
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    st.subheader("📋 All Tasks")

    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    st.session_state.tasks = edited_df.to_dict("records")

    # ------------------- PRIORITIZATION ENGINE -------------------
    st.subheader("⚙ Smart Prioritization Engine")
    df = pd.DataFrame(st.session_state.tasks)
    df["Deadline"] = pd.to_datetime(df["Deadline"])
    df["Days_Left"] = (df["Deadline"] - pd.Timestamp(datetime.today().date())).dt.days
    df["Days_Left"] = df["Days_Left"].apply(lambda x: max(x, 0))

    df_pending = df[df["Completed"] == False].copy()

    if not df_pending.empty:
        scaler = MinMaxScaler()
        df_pending[["Days_Left_Norm", "Difficulty_Norm", "Importance_Norm"]] = scaler.fit_transform(
            df_pending[["Days_Left", "Difficulty", "Importance"]]
        )

        # ------------------- HYBRID PRIORITY SCORING -------------------
        if model:
            df_pending["AI_Priority_Pred"] = model.predict(df_pending[["Difficulty", "Importance"]])
            df_pending["Priority_Score"] = (
                0.5 * (1 - df_pending["Days_Left_Norm"]) +
                0.5 * (df_pending["AI_Priority_Pred"] / 3)
            )
        else:
            df_pending["Priority_Score"] = (
                0.5 * (1 - df_pending["Days_Left_Norm"]) +
                0.3 * df_pending["Importance_Norm"] +
                0.2 * (1 - df_pending["Difficulty_Norm"])
            )

        # Confidence level
        def get_confidence(score):
            if score >= 0.8:
                return "🔥 High"
            elif score >= 0.5:
                return "⚖️ Moderate"
            else:
                return "❄️ Low"

        df_pending["Confidence"] = df_pending["Priority_Score"].apply(get_confidence)

        # Estimated and daily hours
        df_pending["Estimated_Hours"] = round((df_pending["Difficulty"] * df_pending["Importance"]) / 4, 1)
        df_pending["Daily_Hours"] = df_pending.apply(
            lambda x: round(x["Estimated_Hours"] / (x["Days_Left"] if x["Days_Left"] > 0 else 1), 1), axis=1
        )

        # Status
        def get_status(score):
            if score >= 0.75:
                return "🔴 Urgent"
            elif score >= 0.5:
                return "🟡 Upcoming"
            else:
                return "🟢 Safe"

        df_pending["Status"] = df_pending["Priority_Score"].apply(get_status)
        df_pending = df_pending.sort_values(by="Priority_Score", ascending=False)

        st.success("✅ Smart prioritization and schedule created!")

        # ------------------- DISPLAY TABLE -------------------
        st.subheader("🏆 Recommended Order")
        st.dataframe(
            df_pending[["Task", "Deadline", "Days_Left", "Estimated_Hours", "Daily_Hours", "Status", "Confidence"]],
            use_container_width=True
        )

        # ------------------- EVALUATION METRICS -------------------
        st.subheader("📈 Evaluation Metrics")
        avg_confidence = df_pending["Priority_Score"].mean()
        avg_confidence = min(max(avg_confidence, 0.0), 1.0)  # avoid >1 or <0
        reliability = round(avg_confidence * 100, 2)
        st.metric("System Reliability", f"{reliability}%")
        st.progress(avg_confidence)

        # ------------------- DOWNLOAD EXCEL -------------------
        st.subheader("📥 Export Prioritized List")
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_pending.to_excel(writer, index=False, sheet_name="Prioritized_Tasks")
        st.download_button("📂 Download as Excel", data=buffer,
                           file_name="Prioritized_Tasks.xlsx", mime="application/vnd.ms-excel")

        # ------------------- VISUAL DASHBOARD -------------------
        st.subheader("📊 Task Analytics Dashboard")
        col1, col2 = st.columns(2)

        urgency_counts = df_pending["Status"].value_counts().reset_index()
        urgency_counts.columns = ["Status", "Count"]
        urgency_colors = {"🔴 Urgent": "#e63946", "🟡 Upcoming": "#f4a261", "🟢 Safe": "#2a9d8f"}

        with col1:
            chart1 = (
                alt.Chart(urgency_counts, width=270, height=270)
                .mark_arc(innerRadius=60)
                .encode(
                    theta=alt.Theta("Count:Q"),
                    color=alt.Color("Status:N",
                        scale=alt.Scale(domain=list(urgency_colors.keys()), range=list(urgency_colors.values())),
                        legend=alt.Legend(title="Urgency Level")),
                    tooltip=["Status", "Count"]
                )
                .properties(title="Urgency Distribution")
            )
            st.altair_chart(chart1.configure_view(stroke=None).interactive(), use_container_width=True)

        df_all = pd.DataFrame(st.session_state.tasks)
        comp_counts = df_all["Completed"].value_counts().reset_index()
        comp_counts.columns = ["Completed", "Count"]
        comp_counts["Status"] = comp_counts["Completed"].map({True: "✅ Completed", False: "🕓 Pending"})
        completion_colors = {"✅ Completed": "#43aa8b", "🕓 Pending": "#f8961e"}

        with col2:
            chart2 = (
                alt.Chart(comp_counts, width=270, height=270)
                .mark_bar(size=70)
                .encode(
                    x=alt.X("Status:N", title=None, sort=["✅ Completed", "🕓 Pending"]),
                    y=alt.Y("Count:Q", title="Number of Tasks"),
                    color=alt.Color("Status:N",
                        scale=alt.Scale(domain=list(completion_colors.keys()), range=list(completion_colors.values())),
                        legend=alt.Legend(title="Task Status")),
                    tooltip=["Status", "Count"]
                )
                .properties(title="Task Completion Summary")
            )
            st.altair_chart(chart2.configure_view(stroke=None).interactive(), use_container_width=True)

        # ------------------- AI STUDY ASSISTANT -------------------
        st.subheader("🤖 AI Study Assistant")
        try:
            summarizer = pipeline("summarization", model="google/flan-t5-base")
            if st.button("🧠 Generate Study Strategy"):
                combined_tasks = ". ".join(
                    df_pending.apply(lambda x: f"{x['Task']} (Difficulty {x['Difficulty']}, Importance {x['Importance']})", axis=1)
                )
                summary = summarizer(combined_tasks, max_length=80, min_length=30, do_sample=False)
                st.info(f"🪄 **AI Suggestion:** {summary[0]['summary_text']}")
        except Exception as e:
            st.warning("⚠️ AI Assistant unavailable — install 'transformers' or check model loading.")
            st.text(f"Error: {e}")

    else:
        st.info("🎉 All tasks completed or no pending tasks left!")

else:
    st.info("No tasks added yet. Start by adding some above!")

# ------------------- FOOTER -------------------
st.markdown("""
<br><hr>
<center style='color: #333; font-family: Poppins, sans-serif;'>
Developed by <b>Kanishka Gupta</b> | IIT Roorkee 🎓 <br>
<a href='mailto:kanishka@example.com' style='text-decoration:none; color:#6a11cb;'>Contact</a> |
<a href='https://streamlit.io' style='text-decoration:none; color:#2575fc;'>Powered by Streamlit</a> |
© 2025 Academic Task Prioritizer
</center>
""", unsafe_allow_html=True)
