# 해당 코드는 강의를 보고 만들었습니다.
# 학습을 위해 이곳에 임시 저장합니다
# 나만의 투두리스트앱

import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "task.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
                for task in tasks:
                    listbox.insert(tk.END, task)
            except json.JSONDecodeError:
                pass

    else:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_task():
    tasks =listbox.get(0, tk.END)
    with open(DATA_FILE, 'w', encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def add_task(event=None):
    task = entry.get().strip()
    if task:
        listbox.insert(tk.END, "☐ "+task)
        entry.delete(0, tk.END)
        save_task()
    else:
        messagebox.showwarning("Input error!", "목록을 입력하세요.")

def del_task():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        save_task()
    except IndexError:
        messagebox.showwarning("Warning", "삭제할 목록을 선택하세요.")

def toggle_task():
    try:
        index = listbox.curselection()[0]
        task = listbox.get(index)

        if task.startswith("☑"):
            new_task = task.replace("☑", "☐", 1)
        else:
            new_task = task.replace("☐", "☑", 1)

        listbox.delete(index)
        listbox.insert(index, new_task)

        save_task()

    except IndexError:
        messagebox.showwarning("Warning", "목록을 선택하세요.")



root = tk.Tk()
root.title("To Do List")
root.geometry("420x500")

# Entry box
entry = tk.Entry(root, width=30, bg="ivory",
                 justify="center",
                 font=("", 12, "bold"))
entry.pack(pady=10, ipady=8)
# 엔터키로 입력 가능
entry.bind("<Return>", add_task)

# Buttons
add_button = tk.Button(
    root, 
    text="Add Task", 
    width=15, 
    command=add_task,
    font=("Times New Roman", 15, "bold"),
    bg="#1BA0F3", 
    fg="white")
add_button.pack(pady=5)

delete_button = tk.Button(
    root, 
    text="Delete Task" ,
    width=15, command=del_task,
    font=("Times New Roman", 15, "bold"),
    bg="#05A95D", 
    fg="white")
delete_button.pack(pady=5)

complete_button = tk.Button(
    root,
    text="Complete",
    width=15,
    command=toggle_task,
    font=("Times New Roman", 15, "bold"),
    bg="#F39C12",
    fg="white")

complete_button.pack(pady=5)

# scroballbar
scroballbar = tk.Scrollbar(root)
scroballbar.pack(side="right", fill="y")
# Listbox
listbox= tk.Listbox(root, font=("", 14, "bold"), width=35, height=12, 
                    bg= "ivory", fg="brown", selectmode=tk.SINGLE)
listbox.pack(pady=10)
# 더블 클릭으로 삭제 가능
listbox.bind("<Double-Button-1>", lambda e: toggle_task())
listbox.config(yscrollcommand=scroballbar.set)
scroballbar.config(command=listbox.yview)
load_tasks()
root.mainloop()
