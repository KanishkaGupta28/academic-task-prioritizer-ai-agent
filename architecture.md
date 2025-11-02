#  AI Agent Architecture — Academic Task Prioritizer

## Overview
The **Academic Task Prioritizer AI Agent** automates the process of managing and prioritizing academic tasks.  
It simulates reasoning, planning, and evaluation — similar to an intelligent assistant — to help students efficiently plan their study schedules.

---

##  Core Components

| Component | Description |
|------------|-------------|
| **1. Input Layer** | Collects task details such as name, deadline, difficulty, and importance through an interactive Streamlit form. |
| **2. Preprocessing Module** | Converts deadlines into “days left” and normalizes numerical values using `MinMaxScaler` for balanced comparison. |
| **3. AI Reasoning Engine** | Uses the **fine-tuned regression model (`fine_tuned_model.pkl`)** to calculate priority scores based on difficulty and importance. |
| **4. Planning Engine** | Generates a personalized study plan with estimated total and daily hours per task. |
| **5. Evaluation System** | Calculates **reliability**, **confidence**, and **consistency** of AI outputs to measure reasoning quality. |
| **6. Visualization Layer** | Displays urgency distribution and completion analytics using Altair charts. |
| **7. Export & Persistence Layer** | Allows users to export results to Excel for offline access. |

---

## Architecture Flow (Visual Diagram)

![AI Agent Architecture Diagram](architecture_diagram.png)

---

##  Design Justification

- **Reasoning Logic:**  
  The model integrates a fine-tuned regression model trained on academic task data.  
  It improves prioritization accuracy and mimics intelligent reasoning using weighted scoring.

- **Planning Strategy:**  
  Uses task deadlines, difficulty, and importance to calculate realistic **daily study hours**.  
  This helps students maintain balance between urgency and workload.

- **Evaluation Metrics:**  
  Includes **System Reliability (%)**, **Confidence Score**, and progress indicators to assess the agent’s decision quality.

---

##  Technology Stack

| Layer | Tools Used |
|--------|-------------|
| **Frontend (UI)** | Streamlit |
| **Data Handling** | Pandas |
| **Normalization** | Scikit-learn (`MinMaxScaler`) |
| **Fine-Tuned Model** | Scikit-learn Regression Model (`fine_tuned_model.pkl`) |
| **Visualization** | Altair |
| **Export** | XlsxWriter |
| **Language** | Python 3.10+ |

---

##  Integration and Fine-Tuning

- The agent integrates a **fine-tuned regression model** that adapts to academic workload prioritization.  
- Future upgrades can include **LoRA** or transformer-based models for adaptive learning behavior.  
- Additional modules such as **Planner Agent** or **Reminder Agent** can be integrated for automation and scheduling.

---

##  Key Takeaways

- The AI agent now **reasons**, **plans**, and **evaluates** using a trained ML model.  
- The architecture is **modular**, **scalable**, and **explainable**, ensuring transparency in prioritization.  
- The visual and analytical layers make it practical for real-world academic task management.

---

