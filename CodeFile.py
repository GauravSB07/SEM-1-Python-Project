
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# ================= COLORS ================
BG_COLOR = "#e6e6fa"
BTN_COLOR = "#7b638c"
BTN_HOVER = "#4B0082"
TEXT_COLOR = "#4B0082"
HEADING_COLOR = "#2c3e50"
SUCCESS_COLOR = "#734f96"
ERROR_COLOR = "#e74c3c"

current_teacher = None
DEPARTMENTS_FILE = "departments.json"
TEACHERS_FILE = "teachers.json"
RESULTS_FILE = "results.json"

DEFAULT_DEPARTMENTS = {
    "Biotechnology": ["Genetics", "Molecular Biology"],
    "Computer Science": ["C Programming", "Python", "Java"],
    "Microbiology": ["Immunology", "Virology"]
}
# ----------------- Utilities -----------------
def slug(s: str) -> str:
    return "_".join(s.strip().split()).lower()

#-------------------helper---------------------
def on_enter(e): 
    try:
        e.widget["background"] = BTN_HOVER
    except Exception:
        pass

def on_leave(e): 
    try:
        e.widget["background"] = BTN_COLOR
    except Exception:
        pass

def styled_button(frame, text, cmd, width=20, height=2):
    btn = tk.Button(frame, text=text, width=width, height=height, bg=BTN_COLOR, fg="white",
                    font=("Arial", 11, "bold"), activebackground=BTN_HOVER, activeforeground="white",
                    command=cmd, bd=0, relief="flat", cursor="hand2")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def entry_with_label(frame, text, width=30):
    tk.Label(frame, text=text, font=("Arial", 11), fg=TEXT_COLOR, bg=BG_COLOR).pack()
    entry = tk.Entry(frame, width=width, font=("Arial", 11))
    entry.pack()
    return entry


def load_departments():

    if os.path.exists(DEPARTMENTS_FILE):
        try:
            data = json.load(open(DEPARTMENTS_FILE, "r", encoding="utf-8"))
            
            if isinstance(data, dict):
                
                for k, v in DEFAULT_DEPARTMENTS.items():
                    if k not in data:
                        data[k] = v.copy()
                return data
            
            if isinstance(data, list):
                result = {}
                for item in data:
                    if item in DEFAULT_DEPARTMENTS:
                        result[item] = DEFAULT_DEPARTMENTS[item].copy()
                    else:
                        result[item] = []
                
                for k, v in DEFAULT_DEPARTMENTS.items():
                    if k not in result:
                        result[k] = v.copy()
                save_departments(result)
                return result
        except Exception:
            pass

    save_departments(DEFAULT_DEPARTMENTS.copy())
    return DEFAULT_DEPARTMENTS.copy()

def save_departments(data: dict):
    with open(DEPARTMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_teachers_db():
    if os.path.exists(TEACHERS_FILE):
        try:
            return json.load(open(TEACHERS_FILE, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_teachers_db(db: dict):
    with open(TEACHERS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            return json.load(open(RESULTS_FILE, "r", encoding="utf-8"))
        except Exception:
            return []
    return []

def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def question_filename(dept: str, subject: str) -> str:
    return f"{slug(dept)}__{slug(subject)}.json"


# ----------------- Main Menu -----------------
def show_main_menu(frame):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text="Welcome to the Quiz App", font=("Arial", 20, "bold"),
             fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=20)
    styled_button(frame, "Teacher", lambda: teacher_username(frame)).pack(pady=10)
    styled_button(frame, "Student", lambda: student_departments(frame)).pack(pady=10)


# ----------------- Teacher Flow -----------------
def teacher_username(frame):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)

    departments = load_departments()
    dept_names = sorted(departments.keys())

    tk.Label(frame, text="Select Department", font=("Arial", 14, "bold"),
             fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

    selected_dept = tk.StringVar(value=dept_names[0] if dept_names else "")
    dept_menu = tk.OptionMenu(frame, selected_dept, *dept_names)
    dept_menu.config(font=("Arial", 12), bg=BTN_COLOR, fg="white", width=25)
    dept_menu.pack(pady=5)

    tk.Label(frame, text="Enter Username", font=("Arial", 12, "bold"),
             fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=5)
    username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)

    def add_department_window():
        for w in frame.winfo_children(): w.destroy()
        frame.config(bg=BG_COLOR)

        tk.Label(frame, text="Department Name", font=("Arial", 12), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=6)
        name_e = tk.Entry(frame, font=("Arial", 12), width=30); name_e.pack(pady=4)
        tk.Label(frame, text="Comma-separated default subjects (optional)", font=("Arial", 10), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=4)
        subj_e = tk.Entry(frame, font=("Arial", 10), width=40); subj_e.pack(pady=4)

        def save_new_dept():
            name = name_e.get().strip()
            if not name:
                messagebox.showerror("Error", "Department name cannot be empty", parent=frame); return
            depts = load_departments()
            if name in depts:
                messagebox.showwarning("Warning", "Department already exists", parent=frame); return
            subs_raw = subj_e.get().strip()
            if subs_raw:
                subs = [s.strip() for s in subs_raw.split(",") if s.strip()]
            else:
                subs = []
            depts[name] = subs
            save_departments(depts)
            messagebox.showinfo("Success", f"Department '{name}' added", parent=frame)
            teacher_username(frame)  

        styled_button(frame, "Save Department", save_new_dept).pack(pady=8)
        styled_button(frame, "Cancel", lambda: teacher_username(frame)).pack()

    styled_button(frame, "Add Department", add_department_window).pack(pady=6)

    def continue_click():
        dept = selected_dept.get()
        user = username_entry.get().strip()
        if not user:
            messagebox.showerror("Error", "Please enter a username")
            return
        global current_teacher
        current_teacher = {"department": dept, "username": user}
        check_password(frame)

    styled_button(frame, "Continue", continue_click).pack(pady=10)
    styled_button(frame, "Back", lambda: show_main_menu(frame)).pack(pady=5)

    
def check_password(frame):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)

    tk.Label(frame, text="Enter Department Password", font=("Arial", 14, "bold"),
             fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.pack(pady=5)

    def verify():
        global current_teacher
        if not isinstance(current_teacher, dict):
            messagebox.showerror("Error", "Internal error: current_teacher corrupted"); return
            
        dept = current_teacher["department"]
        user = current_teacher["username"]

        teachers_db = load_teachers_db()
        if dept not in teachers_db:
            
            teachers_db[dept] = {"password": password_entry.get(), "teachers": [user]}
            save_teachers_db(teachers_db)
            messagebox.showinfo("Registered", f"Department '{dept}' password set and teacher '{user}' registered")
            subjects(frame, dept)
            return

        if teachers_db[dept].get("password") == password_entry.get():
            if user not in teachers_db[dept].get("teachers", []):
                teachers_db[dept].setdefault("teachers", []).append(user)
                save_teachers_db(teachers_db)
                messagebox.showinfo("Added", f"Teacher '{user}' added to {dept}")
            subjects(frame, dept)
        else:
            messagebox.showerror("Error", "Incorrect password")

    styled_button(frame, "Login", verify).pack(pady=10)
    styled_button(frame, "Back", lambda: teacher_username(frame)).pack(pady=5)

# ----------------- Subjects (teacher) -----------------
def subjects(frame, dept):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Subjects — {dept}", font=("Arial", 16, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=12)

    depts = load_departments()
    subs = depts.get(dept, [])

    if not subs:
        tk.Label(frame, text="No subjects yet. Add one.", fg=ERROR_COLOR, bg=BG_COLOR).pack(pady=8)
    else:
        for s in subs:
            styled_button(frame, s, lambda subj=s: teacher_interface(frame, dept, subj)).pack(pady=6)

    styled_button(frame, "Add New Subject", lambda: add_new_subject(frame, dept)).pack(pady=10)
    styled_button(frame, "Back", lambda: check_password(frame)).pack(pady=5)

def add_new_subject(frame, dept):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Add Subject — {dept}", font=("Arial", 14, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)
    subject_entry = tk.Entry(frame, font=("Arial", 12), width=30); subject_entry.pack(pady=5)

    def save_subject():
        new_subject = subject_entry.get().strip()
        if not new_subject:
            messagebox.showerror("Error", "Subject name cannot be empty"); return
            
        depts = load_departments()
        subs = depts.get(dept, [])
        if new_subject in subs:
            messagebox.showwarning("Warning", "Subject already exists"); return
        subs.append(new_subject)
        depts[dept] = subs
        save_departments(depts)
       
        qfile = question_filename(dept, new_subject)
        with open(qfile, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        messagebox.showinfo("Success", f"Subject '{new_subject}' added to {dept}")
        subjects(frame, dept)

    styled_button(frame, "Save", save_subject).pack(pady=8)
    styled_button(frame, "Back", lambda: subjects(frame, dept)).pack(pady=4)


# ----------------- Teacher: Manage Questions / View Results -----------------
def teacher_interface(frame, dept, subject):
    for w in frame.winfo_children(): w.destroy()
    
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Logged in as: {current_teacher['username']} ({dept})",
             font=("Arial", 11, "italic"), fg=SUCCESS_COLOR, bg=BG_COLOR).pack(pady=6)
    tk.Label(frame, text=f"Add Question — {subject}", font=("Arial", 14, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=10)

    question_entry = entry_with_label(frame, "Question:")
    opt1 = entry_with_label(frame, "Option 1:")
    opt2 = entry_with_label(frame, "Option 2:")
    opt3 = entry_with_label(frame, "Option 3:")
    opt4 = entry_with_label(frame, "Option 4:")
    correct = entry_with_label(frame, "Correct Option (1-4):", width=6)
    time_entry=entry_with_label(frame,"Time(seconds):",width=6)

    def save_question():
        q = question_entry.get().strip()
        opts = [opt1.get().strip(), opt2.get().strip(), opt3.get().strip(), opt4.get().strip()]
        corr = correct.get().strip()
        t=time_entry.get().strip()
        
        if not q or "" in opts or not corr.isdigit():
            messagebox.showerror("Error", "Fill all fields correctly"); return
            
        cidx = int(corr) - 1
        
        if cidx not in range(4):
            messagebox.showerror("Error", "Correct option must be 1-4"); return
        
        try:
            time_sec=int(t)
        except Exception:
            messagebox.showerror("Error","Invalid time value"); return

        if time_sec<=0:
          messagebox.showerror("Error","Time must be greater than 0")
          return
        qfile = question_filename(dept, subject)
        
        try:
            questions = json.load(open(qfile, "r", encoding="utf-8")) if os.path.exists(qfile) else []
        except Exception:
            questions = []
        questions.append({"question": q, "options": opts, "answer": opts[cidx],"time":time_sec})
        with open(qfile, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Success", "Question added")
        teacher_interface(frame, dept, subject)

    styled_button(frame, "Save Question", save_question).pack(pady=8)
    styled_button(frame, "Manage Questions", lambda: manage_questions(frame, dept, subject)).pack(pady=6)
    styled_button(frame, "View Results", lambda: view_results(frame, dept, subject)).pack(pady=6)
    styled_button(frame, "Back to Subjects", lambda: subjects(frame, dept)).pack(pady=6)

def manage_questions(frame, dept, subject):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Manage Questions — {subject} ({dept})", font=("Arial", 14, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=10)

    qfile = question_filename(dept, subject)
    if not os.path.exists(qfile):
        tk.Label(frame, text="No questions file found.", fg=ERROR_COLOR, bg=BG_COLOR).pack(pady=8)
        styled_button(frame, "Back", lambda: teacher_interface(frame, dept, subject)).pack(pady=6)
        return

    try:
        questions = json.load(open(qfile, "r", encoding="utf-8"))
    except Exception:
        questions = []

    if not questions:
        tk.Label(frame, text="No questions available.", fg=ERROR_COLOR, bg=BG_COLOR).pack(pady=8)
        styled_button(frame, "Back", lambda: teacher_interface(frame, dept, subject)).pack(pady=6)
        return

    for idx, q in enumerate(questions):
        tk.Label(frame, text=f"Q{idx+1}: {q['question']}", wraplength=460, justify="left", fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", padx=10, pady=2)
        btnf = tk.Frame(frame, bg=BG_COLOR); btnf.pack(pady=4)
        styled_button(btnf, "Edit", lambda i=idx: edit_question(frame, dept, subject, i)).pack(side="left", padx=4)
        styled_button(btnf, "Delete", lambda i=idx: delete_question(frame, dept, subject, i)).pack(side="left", padx=4)

    styled_button(frame, "Back", lambda: teacher_interface(frame, dept, subject)).pack(pady=10)

def edit_question(frame, dept, subject, index):
    qfile = question_filename(dept, subject)
    try:
        questions = json.load(open(qfile, "r", encoding="utf-8"))
    except Exception:
        messagebox.showerror("Error", "Cannot open questions file"); manage_questions(frame, dept, subject); return

    if index < 0 or index >= len(questions):
        messagebox.showerror("Error", "Invalid question index"); manage_questions(frame, dept, subject); return

    qdata = questions[index]
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Edit Q{index+1} — {subject}", font=("Arial", 14, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=10)

    question_entry = entry_with_label(frame, "Question:"); question_entry.insert(0, qdata.get("question",""))
    opt_entries = []
    for i in range(4):
        e = entry_with_label(frame, f"Option {i+1}:"); e.insert(0, qdata.get("options", [""]*4)[i])
        opt_entries.append(e)
    correct_entry = entry_with_label(frame, "Correct Option (1-4):", width=6)
    try:
        correct_entry.insert(0, str(qdata["options"].index(qdata["answer"])+1))
    except Exception:
        correct_entry.insert(0, "1")
    time_entry=entry_with_label(frame,"Time(seconds):",width=6)
    time_entry.insert(0,str(qdata.get("time",15)))

    def save_edit():
        nq = question_entry.get().strip()
        nopts = [e.get().strip() for e in opt_entries]
        if not nq or "" in nopts:
            messagebox.showerror("Error", "Fields cannot be empty"); return
        try:
            nc = int(correct_entry.get().strip()) - 1
            nt=int(time_entry.get().strip())
        except Exception:
            messagebox.showerror("Error", "Correct option must be 1-4"); return
        if nc not in range(4) or nt<=0:
            messagebox.showerror("Error", "Correct option must be 1-4 and time>0"); return
        questions[index] = {"question": nq, "options": nopts, "answer": nopts[nc],"time":nt}
        with open(qfile, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Success", "Question updated")
        manage_questions(frame, dept, subject)

    styled_button(frame, "Save", save_edit).pack(pady=8)
    styled_button(frame, "Back", lambda: manage_questions(frame, dept, subject)).pack(pady=4)

def delete_question(frame, dept, subject, index):
    qfile = question_filename(dept, subject)
    try:
        questions = json.load(open(qfile, "r", encoding="utf-8"))
    except Exception:
        messagebox.showerror("Error", "Cannot open questions file"); manage_questions(frame, dept, subject); return
    if 0 <= index < len(questions):
        questions.pop(index)
        with open(qfile, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Deleted", "Question removed")
    else:
        messagebox.showerror("Error", "Invalid index")
    manage_questions(frame, dept, subject)

def view_results(frame, dept, subject):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Results — {subject} ({dept})", font=("Arial", 14, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=10)
    results = load_results()
    
    filtered = [r for r in results if 
                r.get("department")== dept and 
                r.get("subject")==subject]
    
    if not filtered:
        tk.Label(frame, text="No results yet.", fg=ERROR_COLOR, bg=BG_COLOR).pack(pady=8)
    else:
        for r in filtered:
            text = f"{r.get('student','Anonymous')}: {r.get('score',0)} / {r.get('total',0)}"
            tk.Label(frame, text=text, fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", padx=10, pady=2)
    styled_button(frame, "Back", lambda: teacher_interface(frame, dept, subject)).pack(pady=10)

# ----------------- Student Flow -----------------
def student_departments(frame):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text="Select Department", font=("Arial", 16, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=12)
    depts = load_departments()
    
    for d in sorted(depts.keys()):
        styled_button(frame, d, lambda dept=d: student_subjects(frame, dept)).pack(pady=6)
    styled_button(frame, "Back", lambda: show_main_menu(frame)).pack(pady=6)

def student_subjects(frame, dept):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"Select Subject — {dept}", font=("Arial", 16, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=12)
    depts = load_departments()
    subs = depts.get(dept, [])
    if not subs:
        tk.Label(frame, text="No subjects available.", fg=ERROR_COLOR, bg=BG_COLOR).pack(pady=8)
    else:
        for s in subs:
            styled_button(frame, s, lambda subj=s: student_interface(frame, dept, subj)).pack(pady=6)
    styled_button(frame, "Back", lambda: student_departments(frame)).pack(pady=6)

def student_interface(frame, dept, subject):
    for w in frame.winfo_children(): w.destroy()
    frame.config(bg=BG_COLOR)
    tk.Label(frame, text=f"{subject} — {dept}", font=("Arial", 14, "bold"), fg=HEADING_COLOR, bg=BG_COLOR).pack(pady=8)
    qfile = question_filename(dept, subject)
    if not os.path.exists(qfile):
        messagebox.showerror("Error", f"No quiz found for {subject}"); student_subjects(frame, dept); return
    try:
        questions = json.load(open(qfile, "r", encoding="utf-8"))
    except Exception:
        questions = []
    if not questions:
        messagebox.showerror("Error", "No questions in this quiz yet"); student_subjects(frame, dept); return

    
    score = 0
    index = 0
    total = len(questions)
    timer_id = None  

    def finish_and_save():
        nonlocal score, index
        student_name = simpledialog.askstring("Your Name", "Enter your name (optional):", parent=frame)
        if not student_name:
            student_name = "Anonymous"
        new_result = {"student": student_name, "department": dept, "subject": subject, "score": score, "total": total}
        results = load_results()
        results.append(new_result)
        save_results(results)
        messagebox.showinfo("Result Saved", f"{student_name}, you scored {score} / {total}")
        student_subjects(frame, dept)

    def load_question():
        nonlocal index, score, timer_id
        
        if timer_id is not None:
            try:
                frame.after_cancel(timer_id)
            except Exception:
                pass
            timer_id = None

        for w in frame.winfo_children(): w.destroy()
        frame.config(bg=BG_COLOR)

        if index >= total:
            finish_and_save()
            return

        q = questions[index]
        time_left = q.get("time", 15)

        tk.Label(frame, text=f"Q{index+1}: {q['question']}", wraplength=460,
                 font=("Arial", 12, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

        
        def check_answer(selected, correct):
            nonlocal index, score, timer_id
            
            if timer_id is not None:
                try:
                    frame.after_cancel(timer_id)
                except Exception:
                    pass
                timer_id = None
            if selected == correct:
                score += 1
            index += 1
            load_question()

        
        for opt in q["options"]:
            styled_button(frame, opt, lambda o=opt: check_answer(o, q["answer"])).pack(pady=6)

        timer_label = tk.Label(frame, text=f"Time left: {time_left}s", font=("Arial", 12, "bold"), fg=ERROR_COLOR, bg=BG_COLOR)
        timer_label.pack(pady=10)
        styled_button(frame, "Quit", lambda: (
            frame.after_cancel(timer_id) if timer_id is not None else None,
            student_subjects(frame, dept)
        )).pack(pady=8)

        def update_timer():
            nonlocal time_left, index, timer_id
            if time_left <= 0:
                
                timer_id = None
                index += 1
                load_question()
                return
            timer_label.config(text=f"Time left: {time_left}s")
            time_left -= 1
            timer_id = frame.after(1000, update_timer)

        update_timer()

    load_question()

# ----------------- Main Loop -----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("560x640")
    root.config(bg=BG_COLOR)

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    show_main_menu(main_frame)
    root.mainloop()
