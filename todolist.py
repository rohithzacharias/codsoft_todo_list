import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import pandas as pd
import os

# Initialize window
root = tk.Tk()
root.title("Smart To-Do List App")
root.geometry("850x600")

# Global list to store tasks
tasks = []

# Categories mapping
category_options = {
    "Important & Urgent": "🔴 Important & Urgent",
    "Important but Not Urgent": "🟡 Important but Not Urgent",
    "Not Important but Urgent": "🟢 Not Important but Urgent",
    "Not Important & Not Urgent": "⚪ Not Important & Not Urgent"
}

# Load tasks from Excel if exists
EXCEL_FILE = "tasks.xlsx"
def load_tasks():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        for _, row in df.iterrows():
            try:
                tasks.append({
                    "title": row["Task"],
                    "category": row["Category"],
                    "deadline": datetime.strptime(row["Deadline"], "%Y-%m-%d %I:%M %p"),
                    "status": row.get("Status", "Pending")
                })
            except:
                continue

# Save tasks to Excel
def save_tasks():
    df = pd.DataFrame([{
        "Category": task["category"],
        "Task": task["title"],
        "Deadline": task["deadline"].strftime("%Y-%m-%d %I:%M %p"),
        "Status": task["status"]
    } for task in tasks])
    df.to_excel(EXCEL_FILE, index=False)

# Frame setup
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

frame_mid = tk.Frame(root)
frame_mid.pack(pady=10)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

# Task input fields
category_label = tk.Label(frame_top, text="Category:")
category_label.grid(row=0, column=0)
category_var = tk.StringVar(value=list(category_options.keys())[0])
category_menu = ttk.Combobox(frame_top, textvariable=category_var, values=list(category_options.keys()), state='readonly', width=30)
category_menu.grid(row=0, column=1, padx=5)

task_entry_label = tk.Label(frame_top, text="Task:")
task_entry_label.grid(row=1, column=0)
task_entry = tk.Entry(frame_top, width=40)
task_entry.grid(row=1, column=1, padx=5)

deadline_label = tk.Label(frame_top, text="Deadline (YYYY-MM-DD HH:MM):")
deadline_label.grid(row=2, column=0)
deadline_entry = tk.Entry(frame_top, width=25)
deadline_entry.grid(row=2, column=1, padx=5)

ampm_label = tk.Label(frame_top, text="AM/PM:")
ampm_label.grid(row=2, column=2)
ampm_var = tk.StringVar(value="AM")
ampm_menu = ttk.Combobox(frame_top, textvariable=ampm_var, values=["AM", "PM"], state='readonly', width=5)
ampm_menu.grid(row=2, column=3, padx=5)

# Task list display
tree = ttk.Treeview(frame_mid, columns=("Category", "Task", "Deadline", "Time Left", "Status"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack()

# Function to update tree
def refresh_tree():
    tree.delete(*tree.get_children())
    now = datetime.now()
    for task in tasks:
        remaining = task["deadline"] - now
        if remaining.total_seconds() < 0:
            time_left = "❌ Missed"
            task["status"] = "Missed"
        else:
            time_left = str(remaining).split('.')[0]
            # Trigger reminders
            if task["status"] == "Pending":
                if remaining <= timedelta(minutes=10):
                    if int(now.second) == 0:  # Only once per minute
                        messagebox.showinfo("Reminder", f"Last 10 minutes for: {task['title']}")
                elif remaining <= timedelta(hours=1):
                    if now.minute % 10 == 0 and now.second == 0:
                        messagebox.showinfo("Reminder", f"Last hour for: {task['title']}")
                elif remaining <= timedelta(days=1):
                    if now.minute == 0 and now.second == 0:
                        messagebox.showinfo("Reminder", f"Only 1 day left for: {task['title']}")

        tree.insert("", "end", values=(
            task["category"],
            task["title"],
            task["deadline"].strftime("%Y-%m-%d %I:%M %p"),
            time_left,
            task["status"]
        ))

# Add task function
def add_task():
    title = task_entry.get().strip()
    category = category_var.get()
    deadline_str = deadline_entry.get().strip()
    ampm = ampm_var.get()

    if not title or not deadline_str:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        full_deadline = f"{deadline_str} {ampm}"
        deadline = datetime.strptime(full_deadline, "%Y-%m-%d %I:%M %p")
    except ValueError:
        messagebox.showerror("Invalid Format", "Use format YYYY-MM-DD HH:MM and select AM/PM")
        return

    task = {
        "title": title,
        "category": category_options[category],
        "deadline": deadline,
        "status": "Pending"
    }
    tasks.append(task)
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_tree()
    save_tasks()

# Delete selected task
def delete_task():
    selected = tree.selection()
    if selected:
        index = tree.index(selected[0])
        tasks.pop(index)
        refresh_tree()
        save_tasks()
    else:
        messagebox.showwarning("No selection", "Please select a task to delete.")

# Mark task as completed
def mark_completed():
    selected = tree.selection()
    if selected:
        index = tree.index(selected[0])
        tasks[index]["status"] = "Completed"
        refresh_tree()
        save_tasks()
    else:
        messagebox.showwarning("No selection", "Please select a task to mark as completed.")

# Periodically check for updates
def update_loop():
    def loop():
        refresh_tree()
        save_tasks()
        root.after(60000, loop)  # Run every 60 seconds
    loop()

# Buttons
add_button = tk.Button(frame_bottom, text="Add Task", command=add_task, width=20)
add_button.pack(pady=5)

delete_button = tk.Button(frame_bottom, text="Delete Task", command=delete_task, width=20)
delete_button.pack(pady=5)

complete_button = tk.Button(frame_bottom, text="Mark as Completed", command=mark_completed, width=20)
complete_button.pack(pady=5)

# Load tasks on startup
load_tasks()
refresh_tree()

# Start update loop using Tkinter's after()
update_loop()

root.mainloop()