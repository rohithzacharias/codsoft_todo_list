# 📝 Smart To-Do List App

This is a Python-based **Smart To-Do List App** with a GUI built using Tkinter. It allows users to manage tasks with deadlines, categories, reminders, and status tracking. All tasks are saved to an Excel file for persistence.

## ✅ Features

- **Add, Delete, and Mark Tasks as Completed**
- **Categorize tasks** using the Eisenhower Matrix:
  - 🔴 Important & Urgent
  - 🟡 Important but Not Urgent
  - 🟢 Not Important but Urgent
  - ⚪ Not Important & Not Urgent
- **12-hour time input (AM/PM support)**
- **Live countdown timer** for each task
- **Reminders:**
  - 1-day left: notifies every 10 minutes
  - Final hour: notifies every 10 minutes
- **Excel storage (tasks.xlsx)** for saving and loading tasks

## 🛠️ Built With

- Python 3
- Tkinter
- pandas
- openpyxl

## 📦 Requirements

Install dependencies using pip:

```bash
pip install pandas openpyxl
