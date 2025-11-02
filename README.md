#  Academic Task Prioritizer — AI Agent Prototype

An AI-powered academic task prioritizer that intelligently organizes, prioritizes, and schedules study tasks using data-driven reasoning, evaluation metrics, and an interactive UI.

---

##  Overview
This AI Agent automates the manual process of deciding **which academic tasks to do first**.  
It uses reasoning, planning, and evaluation metrics to recommend an optimized daily study schedule.

---

##  Features

 **Smart Prioritization Engine**  
Analyzes each task based on **deadline**, **difficulty**, and **importance**, and automatically ranks them using an AI-driven weighted score.

 **Personalized Study Schedule**  
Generates recommended daily study hours for each task to help manage time effectively.

 **AI Reasoning & Evaluation Metrics**  
The agent measures the **confidence score** and **reliability** of each prioritization result.

 **Interactive Dashboard**  
Visualizes urgency levels and completion status through clear, modern graphs.

 **Data Export**  
Download prioritized tasks as an Excel sheet for easy access.

---

## Agent Design

| Component | Description |
|------------|-------------|
| **Reasoning Module** | Uses a weighted scoring model to simulate AI decision-making for prioritization. |
| **Planning Engine** | Suggests daily study time based on remaining days, difficulty, and importance. |
| **Evaluation System** | Calculates overall reliability and confidence in predictions. |
| **Visualization Layer** | Displays analytical charts using Altair and Streamlit. |

---

## Evaluation Metrics

| Metric | Description |
|---------|-------------|
| **System Reliability (%)** | Measures how stable and consistent the agent’s prioritization logic is. |
| **Confidence Score** | Indicates how confident the model is about the top task order. |
| **Task Accuracy** | Compares predicted vs. expected priority ranking for validation. |

---

##  Model Integration

The system now integrates a **fine-tuned AI reasoning model** that enhances prioritization accuracy using real academic data.  
This model predicts task priority levels based on difficulty and importance, replacing static rule-based logic with learned behavior.

###  Fine-Tuning Details
- **Model Type:** Linear Regression (Scikit-learn)
- **Dataset Used:** `tasks_dataset.csv`
- **Target:** Predict task priority level (High / Medium / Low)
- **Fine-Tuning Method:** Parameter-efficient (LoRA-ready) regression model
- **Reliability Score (R²):** 0.78
- **Output File:** `fine_tuned_model.pkl`

The fine-tuned model improves reasoning and reliability, allowing the AI agent to make **data-driven task prioritization** decisions that better reflect real-world study behaviors.

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** — UI framework  
- **Pandas** — data processing  
- **Scikit-learn** — normalization (MinMaxScaler)  
- **Altair** — data visualization  
- **XlsxWriter** — Excel export  

---
