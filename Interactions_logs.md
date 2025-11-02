#  Interaction Logs — Development History

This document records the prompts, reasoning, and development interactions used during the creation of the **Academic Task Prioritizer AI Agent**.

---

##  Phase 1: Idea and Problem Selection
**Prompt Example:**
> “Select one manual task from daily life or university work and build an AI agent that can automate it.”

**Decision:**
Automate academic task prioritization — help students organize study workloads.

---

##  Phase 2: Core Logic Development
**Prompt Example:**
> “Write Streamlit code to prioritize tasks based on deadline, difficulty, and importance.”

**Outcome:**
Developed rule-based weighted scoring formula for task ranking.

---

##  Phase 3: Model Fine-Tuning
**Prompt Example:**
> “Fine-tune a small model using sample task data to predict task priority levels.”

**Result:**
- Fine-tuned Linear Regression model (`fine_tuned_model.pkl`)
- Achieved **R² = 0.78**

---

## Phase 4: Evaluation Metrics
**Prompt Example:**
> “Add reliability and confidence evaluation metrics to Streamlit dashboard.”

**Outcome:**
Added:
- System Reliability (%)
- Confidence levels (High / Moderate / Low)
- Real-time visual progress bar

---

##  Phase 5: Final Integration
**Prompt Example:**
> “Integrate fine-tuned model into Streamlit and keep rule-based fallback.”

**Outcome:**
Final app supports both AI model predictions and heuristic reasoning.

---

## Optional Phase: Visualization and Demo
**Prompt Example:**
> “Add graphs and charts to visualize urgency and completion summary.”

**Outcome:**
- Added two Altair charts (Urgency Distribution & Task Completion)
- Export to Excel for reports

---

 All development was guided via iterative interaction with ChatGPT (AI co-developer).
