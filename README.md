# 🔬 Lab Equipment Booking System (CSP-Based)

A professional Graphical User Interface (GUI) desktop application built with Python and Tkinter. This project solves a real-world resource allocation problem by applying a **Constraint Satisfaction Problem (CSP)** algorithm to ensure fair, conflict-free scheduling of lab equipment among students.

---

## 🎯 Key Features & CSP Constraints

To guarantee maximum fairness and operational efficiency, the scheduling backend evaluates every booking request against strict mathematical and logical constraints before approval:

* **Resource Conflict Prevention (No Double Booking):** Ensures no two students can reserve the exact same equipment during overlapping hours.
* **Fairness Allocation Policy:** Restricts any single booking session to a maximum duration of **2 hours** to avoid resource hoarding.
* **Operational Boundary Constraint:** Enforces lab operational limits, automatically restricting slots strictly between standard hours (**09:00 AM to 17:00 PM**).
* **Chronological Logic Check:** Validates that the requested end time occurs strictly after the start time.

---

## 💻 Tech Stack & Architecture

* **Programming Language:** Python 3
* **GUI Framework:** Tkinter (Native Desktop Engine)
* **Algorithmic Paradigm:** Constraint Satisfaction Problem (CSP)
* **UI Layout Strategy:** Fully responsive, overlap-free vertical Grid & LabelFrame mapping tailored for online/local environments.

---

## 🛠️ How to Run Locally

### Prerequisites
Make sure you have Python installed on your system. Tkinter comes bundled with standard Python installations.

### Execution Steps
1. Clone this repository or download the `main.py` file.
2. Open your terminal, command prompt, or Python IDLE in the directory containing the file.
3. Execute the application using the following command:
   ```bash
   python main.py
