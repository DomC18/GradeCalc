import tkinter as tk
import sys
from screeninfo import get_monitors

sys.setrecursionlimit(10**6)

monitor_info = get_monitors()
screen_width = monitor_info[0].width
screen_height = monitor_info[0].height
WIDTH_MULTIPLIER = screen_width/1920
HEIGHT_MULTIPLIER = screen_height/1080

window = tk.Tk()
window.attributes("-fullscreen", True)
def toggle_fullscreen(event):
    state = window.attributes('-fullscreen')
    window.attributes('-fullscreen', not state)
def exit(event):
    window.destroy()

window.bind('<F11>', toggle_fullscreen)
window.bind('<Escape>', exit)

window.geometry('1920x1080')
window.title('Grade Calculator')
window.configure(bg='light blue')
window.resizable(width=False, height=False)

def on_entry_click(event, entry:tk.Entry):
    if entry.get() == "0":
        entry.delete(0, tk.END)

def on_entry_leave(event, entry:tk.Entry):
    if entry.get() == "":
        entry.insert(0, "0")

def get_widget_size(widget):
    width = widget.winfo_width()
    height = widget.winfo_height()
    return width, height

q1_setup_items = []
q1_percent_items = []
q2_setup_items = []
q2_percent_items = []
q1s1_assignment_function_calls = 0
q1s2_assignment_function_calls = 0
q1s3_assignment_function_calls = 0
q1s4_assignment_function_calls = 0
q2s1_assignment_function_calls = 0
q2s2_assignment_function_calls = 0
q2s3_assignment_function_calls = 0
q2s4_assignment_function_calls = 0
q1_grade = tk.IntVar()
q2_grade = tk.IntVar()
final_grade = tk.IntVar()
q1_grade.set(0)
q2_grade.set(0)
final_grade.set(0)


class Assignment:
    num_assignments = 0
    def __init__(self, name="assignment"+str(num_assignments), grade=0, entry:tk.Entry=tk.Entry) -> None:
        self.name = name
        self.grade = grade
        Assignment.num_assignments += 1
        self.assignment_id = Assignment.num_assignments
        self.entry = entry


class Section:
    num_sections = 0
    def __init__(self, name="section"+str(num_sections), section_percent=0) -> None:
        self.name = name
        self.section_percent = section_percent
        self.assignments = []
        self.num_assignments = 0
        self.total = 0
        self.score = 0
        Section.num_sections += 1

    def add_assignment(self, entry:tk.Entry, name="", grade=0) -> None:
        assignment = Assignment(name, grade, entry)
        self.total += assignment.grade
        self.num_assignments += 1
        self.assignments.append(assignment)

    def delete_assignment(self, name):
        for assignment in self.assignments:
            if assignment.name == name:
                self.total -= assignment.grade
                self.num_assignments -= 1
                self.assignments.remove(assignment)

    def get_section_score(self) -> int:
        return int(round(self.total/self.num_assignments, 0))
   
    def get_score_with_percent(self) -> int:
        return self.get_section_score() * self.section_percent


class Quarter:
    def __init__(self, quarter_percent=0.4) -> None:
        self.quarter_percent = quarter_percent
        self.sections = []

    def add_assignment(self, assignment_name="assignment"+str(Assignment.num_assignments), grade=0, section_name="") -> None:
        for section in self.sections:
            if section_name == section.name:
                section.add_assignment(assignment_name, grade)

    def add_section(self, name="section"+str(Section.num_sections), section_percent=0) -> Section:
        section = Section(name, section_percent)
        self.sections.append(section)
        return section

    def verify_percentages(self) -> bool:
        is_valid = False
        total_quarter_percentage = 0
        for section in self.sections:
            total_quarter_percentage += section.section_percent
        is_valid = True if total_quarter_percentage == 1 else False
        return is_valid
   
    def get_quarter_grade(self):
        quarter_grade = 0
        if self.verify_percentages():
            for section in self.sections:
                quarter_grade += section.get_score_with_percent()
            return int(round(quarter_grade, 0))
        else:
            return 0


class Midterm:
    def __init__(self, grade=0, percent=0.2) -> None:
        self.grade = grade
        self.percent = percent


class SemesterGrade:
    def __init__(self) -> None:
        self.quarters = []
        self.midterm = None

    def add_quarter(self, quarter_percent) -> Quarter:
        if len(self.quarters) >= 2:
            return "Two quarters have already been created"
        quarter = Quarter(quarter_percent)
        self.quarters.append(quarter)
        return quarter

    def add_midterm(self, midterm_grade=0, midterm_percent=0.2) -> Midterm:
        if type(self.midterm) == Midterm:
            return "A midterm has already been created"
        midterm = Midterm(midterm_grade, midterm_percent)
        self.midterm = midterm
        return midterm

    def verify_percentages(self) -> bool:
        is_valid = False
        total_percentage = 0
        for section in self.quarters:
            total_percentage += section.quarter_percent
        total_percentage += self.midterm.percent
        is_valid = True if total_percentage == 1 else False
        return is_valid
   
    def get_total_quarter_grade(self):
        total_quarter_grade = 0
        if self.verify_percentages():
            for quarter in self.quarters:
                total_quarter_grade += quarter.get_quarter_grade()*quarter.quarter_percent
            return total_quarter_grade
        else:
            return 0
   
    def get_midterm_grade(self):
        if self.verify_percentages:
            return self.midterm.grade*self.midterm.percent
        else:
            return 0
   
    def get_final_grade(self) -> int:
        final_grade = int(round(self.get_total_quarter_grade() + self.get_midterm_grade(), 0))
        return final_grade


total_grade = SemesterGrade()
Q1 = total_grade.add_quarter(quarter_percent=0.4)
Q1_curr_sections = []
Q1s1:Section
Q1s2:Section
Q1s3:Section
Q1s4:Section
Q2 = total_grade.add_quarter(quarter_percent=0.4)
Q2_curr_sections = []
Q2s1:Section
Q2s2:Section
Q2s3:Section
Q2s4:Section
M1 = total_grade.add_midterm(midterm_percent=0.2)

def clear_sections(isQ1):
    if isQ1:
        Q1.sections = []
        Q1_curr_sections.clear()
    else:
        Q2.sections = []
        Q2_curr_sections.clear()

def add_assign(section:Section, name, entry):
    section.add_assignment(name=name, entry=entry, grade=int(entry.get()) if entry.get()!="" else 0)

def del_assign(section:Section, name, entry:tk.Entry):
    section.delete_assignment(name=name)
    entry.delete(0, tk.END)
    entry.insert(0, "0")

def del_assign_row(isQ1:bool, section:Section, name, entry:tk.Entry, label:tk.Label, verify:tk.Button, delete:tk.Button, cancel:tk.Button):
    global q1s1_assignment_function_calls
    global q1s2_assignment_function_calls
    global q1s3_assignment_function_calls
    global q1s4_assignment_function_calls
    global q2s1_assignment_function_calls
    global q2s2_assignment_function_calls
    global q2s3_assignment_function_calls
    global q2s4_assignment_function_calls
    global Q1s1
    global Q1s2
    global Q1s3
    global Q1s4
    global Q2s1
    global Q2s2
    global Q2s3
    global Q2s4
    if isQ1:
        try:
            if section == Q1s1:
                q1s1_assignment_function_calls -= 1
            elif section == Q1s2:
                q1s2_assignment_function_calls -= 1
            elif section == Q1s3:
                q1s3_assignment_function_calls -= 1
            elif section == Q1s4:
                q1s4_assignment_function_calls -= 1
        except:
            pass
    else:
        if section == Q2s1:
            q2s1_assignment_function_calls -= 1
        elif section == Q2s2:
            q2s2_assignment_function_calls -= 1
        elif section == Q2s3:
            q2s3_assignment_function_calls -= 1
        elif section == Q2s4:
            q2s4_assignment_function_calls -= 1
    del_assign(section=section, name=name, entry=entry)
    label.destroy()
    verify.destroy()
    delete.destroy()
    cancel.destroy()
    entry.destroy()

def q1s1_assignment_setup(num_sections=1):
    global q1s1_assignment_function_calls
    global q1_setup_items

    if num_sections == 1:
        if q1s1_assignment_function_calls < 25:
            assign_id = f"assignment{q1s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(14*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 22), relief="raised", justify="center")
            grade_entry.place(relx=303.36/1920, rely=0.07825+q1s1_assignment_function_calls*(0.03))
            label = tk.Label(width=int(17*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 20), relief="raised")
            label.place(relx=80/1920, rely=0.07825+q1s1_assignment_function_calls*(0.03))
            verify = tk.Button(width=int(7*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 14), command=lambda s=Q1s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="raised")
            verify.place(relx=499.2/1920, rely=0.07825+q1s1_assignment_function_calls*(0.03))
            delete = tk.Button(width=int(8*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 14), relief="raised")
            delete.configure(command=lambda s=Q1s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=578.4/1920, rely=0.07825+q1s1_assignment_function_calls*(0.03))
            cancel = tk.Button(width=int(3*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 14), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.07825+q1s1_assignment_function_calls*(0.03))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s1_assignment_function_calls+=1
    elif num_sections == 2:
        if q1s1_assignment_function_calls < 15:
            assign_id = f"assignment{q1s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s1_assignment_function_calls+=1
    elif num_sections == 3:
        if q1s1_assignment_function_calls < 10:
            assign_id = f"assignment{q1s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s1_assignment_function_calls+=1
    elif num_sections == 4:
        if q1s1_assignment_function_calls < 7:
            assign_id = f"assignment{q1s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.07825+(2+q1s1_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s1_assignment_function_calls+=1

def q1s2_assignment_setup(num_sections=2):
    global q1s2_assignment_function_calls
    global q1_setup_items

    if num_sections == 2:
        if q1s2_assignment_function_calls < 15:
            assign_id = f"assignment{q1s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.5+(2+q1s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.5+(2+q1s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.5+(2+q1s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.5+(2+q1s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.5+(2+q1s2_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s2_assignment_function_calls+=1
    elif num_sections == 3:
        if q1s2_assignment_function_calls < 10:
            assign_id = f"assignment{q1s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.375+(2+q1s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.375+(2+q1s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.375+(2+q1s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.375+(2+q1s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.375+(2+q1s2_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s2_assignment_function_calls+=1
    elif num_sections == 4:
        if q1s2_assignment_function_calls < 7:
            assign_id = f"assignment{q1s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=(0.07825+1*(0.225))+(2+q1s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=(0.07825+1*(0.225))+(2+q1s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=(0.07825+1*(0.225))+(2+q1s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=(0.07825+1*(0.225))+(2+q1s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=(0.07825+1*(0.225))+(2+q1s2_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s2_assignment_function_calls+=1

def q1s3_assignment_setup(num_sections=3):
    global q1s3_assignment_function_calls
    global q1_setup_items

    if num_sections == 3:
        if q1s3_assignment_function_calls < 10:
            assign_id = f"assignment{q1s3_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s3_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=0.675+(2+q1s3_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=0.675+(2+q1s3_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s3, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=0.675+(2+q1s3_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s3, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=0.675+(2+q1s3_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s3, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=0.675+(2+q1s3_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s3_assignment_function_calls+=1
    elif num_sections == 4:
        if q1s3_assignment_function_calls < 7:
            assign_id = f"assignment{q1s3_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s3_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=(0.07825+2*(0.225))+(2+q1s3_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=(0.07825+2*(0.225))+(2+q1s3_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s3, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=(0.07825+2*(0.225))+(2+q1s3_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s3, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=(0.07825+2*(0.225))+(2+q1s3_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s3, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=(0.07825+2*(0.225))+(2+q1s3_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s3_assignment_function_calls+=1

def q1s4_assignment_setup(num_sections=4):
    global q1s4_assignment_function_calls
    global q1_setup_items

    if num_sections == 4:
        if q1s4_assignment_function_calls < 7:
            assign_id = f"assignment{q1s4_assignment_function_calls}"
            assign_label_text = f"Assignment {q1s4_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=465/1920, rely=(0.07825+3*(0.225))+(2+q1s4_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=80/1920, rely=(0.07825+3*(0.225))+(2+q1s4_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q1s4, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=501.5/1920, rely=(0.07825+3*(0.225))+(2+q1s4_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q1s4, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=581/1920, rely=(0.07825+3*(0.225))+(2+q1s4_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=True, s=Q1s4, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=42/1920, rely=(0.07825+3*(0.225))+(2+q1s4_assignment_function_calls)*(0.0235))
            q1_setup_items.append(label)
            q1_setup_items.append(grade_entry)
            q1_setup_items.append(verify)
            q1_setup_items.append(delete)
            q1_setup_items.append(cancel)
            q1s4_assignment_function_calls+=1

def q2s1_assignment_setup(num_sections=1):
    global q2s1_assignment_function_calls
    global q2_setup_items

    if num_sections == 1:
        if q2s1_assignment_function_calls < 25:
            assign_id = f"assignment{q2s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(14*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 22), relief="raised", justify="center")
            grade_entry.place(relx=(303.36+670)/1920, rely=0.07825+q2s1_assignment_function_calls*(0.03))
            label = tk.Label(width=int(17*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 20), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.07825+q2s1_assignment_function_calls*(0.03))
            verify = tk.Button(width=int(7*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 14), command=lambda s=Q2s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="raised")
            verify.place(relx=(499.2+670)/1920, rely=0.07825+q2s1_assignment_function_calls*(0.03))
            delete = tk.Button(width=int(8*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 14), relief="raised")
            delete.configure(command=lambda s=Q2s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(578.4+670)/1920, rely=0.07825+q2s1_assignment_function_calls*(0.03))
            cancel = tk.Button(width=int(3*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 14), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.07825+q2s1_assignment_function_calls*(0.03))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s1_assignment_function_calls+=1
    elif num_sections == 2:
        if q2s1_assignment_function_calls < 15:
            assign_id = f"assignment{q2s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s1_assignment_function_calls+=1
    elif num_sections == 3:
        if q2s1_assignment_function_calls < 10:
            assign_id = f"assignment{q2s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s1_assignment_function_calls+=1
    elif num_sections == 4:
        if q2s1_assignment_function_calls < 7:
            assign_id = f"assignment{q2s1_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s1_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s1, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s1, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s1, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.07825+(2+q2s1_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s1_assignment_function_calls+=1

def q2s2_assignment_setup(num_sections=2):
    global q2s2_assignment_function_calls
    global q2_setup_items

    if num_sections == 2:
        if q2s2_assignment_function_calls < 15:
            assign_id = f"assignment{q2s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.5+(2+q2s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.5+(2+q2s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.5+(2+q2s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.5+(2+q2s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.5+(2+q2s2_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s2_assignment_function_calls+=1
    elif num_sections == 3:
        if q2s2_assignment_function_calls < 10:
            assign_id = f"assignment{q2s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.375+(2+q2s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.375+(2+q2s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.375+(2+q2s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.375+(2+q2s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.375+(2+q2s2_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s2_assignment_function_calls+=1
    elif num_sections == 4:
        if q2s2_assignment_function_calls < 7:
            assign_id = f"assignment{q2s2_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s2_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=(0.07825+1*(0.225))+(2+q2s2_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=(0.07825+1*(0.225))+(2+q2s2_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s2, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=(0.07825+1*(0.225))+(2+q2s2_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s2, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=(0.07825+1*(0.225))+(2+q2s2_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s2, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=(0.07825+1*(0.225))+(2+q2s2_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s2_assignment_function_calls+=1

def q2s3_assignment_setup(num_sections=3):
    global q2s3_assignment_function_calls
    global q2_setup_items

    if num_sections == 3:
        if q2s3_assignment_function_calls < 10:
            assign_id = f"assignment{q2s3_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s3_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=0.675+(2+q2s3_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=0.675+(2+q2s3_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s3, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=0.675+(2+q2s3_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s3, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=0.675+(2+q2s3_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s3, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=0.675+(2+q2s3_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s3_assignment_function_calls+=1
    elif num_sections == 4:
        if q2s3_assignment_function_calls < 7:
            assign_id = f"assignment{q2s3_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s3_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=(0.07825+2*(0.225))+(2+q2s3_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=(0.07825+2*(0.225))+(2+q2s3_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s3, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=(0.07825+2*(0.225))+(2+q2s3_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s3, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=(0.07825+2*(0.225))+(2+q2s3_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s3, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=(0.07825+2*(0.225))+(2+q2s3_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s3_assignment_function_calls+=1

def q2s4_assignment_setup(num_sections=4):
    global q2s4_assignment_function_calls
    global q2_setup_items

    if num_sections == 4:
        if q2s4_assignment_function_calls < 7:
            assign_id = f"assignment{q2s4_assignment_function_calls}"
            assign_label_text = f"Assignment {q2s4_assignment_function_calls+1} Grade:"
            grade_entry = tk.Entry(width=int(3*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 16), relief="raised", justify="center")
            grade_entry.place(relx=(465+670)/1920, rely=(0.07825+3*(0.225))+(2+q2s4_assignment_function_calls)*(0.0235))
            label = tk.Label(width=int(38*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text=assign_label_text, font=("Times New Roman", 14), relief="raised")
            label.place(relx=(80+670)/1920, rely=(0.07825+3*(0.225))+(2+q2s4_assignment_function_calls)*(0.0235))
            verify = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Verify ✔", font=("Times New Roman", 10), command=lambda s=Q2s4, n=assign_id, e=grade_entry : add_assign(s, n, e), relief="solid")
            verify.place(relx=(501.5+670)/1920, rely=(0.07825+3*(0.225))+(2+q2s4_assignment_function_calls)*(0.0235))
            delete = tk.Button(width=int(11*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="red", fg="black", text="Delete X", font=("Times New Roman", 10), relief="solid")
            delete.configure(command=lambda s=Q2s4, n=assign_id, e=grade_entry : del_assign(s, n, e))
            delete.place(relx=(581+670)/1920, rely=(0.07825+3*(0.225))+(2+q2s4_assignment_function_calls)*(0.0235))
            cancel = tk.Button(width=int(4*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="gray", fg="black", text="X", font=("Times New Roman", 10), justify="center", relief="flat")
            cancel.configure(command=lambda b=False, s=Q2s4, n=assign_id, e=grade_entry, l=label, v=verify, d=delete, c=cancel : del_assign_row(b, s, n, e, l, v, d, c))
            cancel.place(relx=(42+670)/1920, rely=(0.07825+3*(0.225))+(2+q2s4_assignment_function_calls)*(0.0235))
            q2_setup_items.append(label)
            q2_setup_items.append(grade_entry)
            q2_setup_items.append(verify)
            q2_setup_items.append(delete)
            q2_setup_items.append(cancel)
            q2s4_assignment_function_calls+=1

def clear_section_buttons(section_buttons):
    for widget in section_buttons:
        widget.destroy()

def verify_percents(*entries:tk.Entry):
    total_percent=0
    for entry in entries:
        total_percent+=int(entry.get())/100 if entry.get()!="" else 0
    return total_percent == 1

def create_sections(isQ1, num_sections, percent_buttons, *entries:tk.Entry):
    global Q1s1
    global Q1s2
    global Q1s3
    global Q1s4
    global Q2s1
    global Q2s2
    global Q2s3
    global Q2s4
    if isQ1:
        if num_sections == 2:
            Q1s1 = Q1.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q1s2 = Q1.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q1_curr_sections.append(Q1s1)
            Q1_curr_sections.append(Q1s2)
            Q1s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s1_label.place(relx=42/1920, rely=0.07825)
            Q1s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s1_assign.configure(command=lambda ns=num_sections: q1s1_assignment_setup(ns))
            Q1s1_assign.place(relx=503/1920, rely=0.0785)
            Q1s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s2_label.place(relx=42/1920, rely=0.5)
            Q1s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s2_assign.configure(command=lambda ns=num_sections: q1s2_assignment_setup(ns))
            Q1s2_assign.place(relx=503/1920, rely=0.5)            
            q1_setup_items.append(Q1s1_label)
            q1_setup_items.append(Q1s1_assign)
            q1_setup_items.append(Q1s2_label)
            q1_setup_items.append(Q1s2_assign)
        elif num_sections == 3:
            Q1s1 = Q1.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q1s2 = Q1.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q1s3 = Q1.add_section(section_percent=int(entries[2].get())/100 if entries[2].get()!="" else 0)
            Q1_curr_sections.append(Q1s1)
            Q1_curr_sections.append(Q1s2)
            Q1_curr_sections.append(Q1s3)
            Q1s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s1_label.place(relx=42/1920, rely=0.07825)
            Q1s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s1_assign.configure(command=lambda ns=num_sections: q1s1_assignment_setup(ns))
            Q1s1_assign.place(relx=503/1920, rely=0.0785)
            Q1s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s2_label.place(relx=42/1920, rely=0.375)
            Q1s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s2_assign.configure(command=lambda ns=num_sections: q1s2_assignment_setup(ns))
            Q1s2_assign.place(relx=503/1920, rely=0.375)
            Q1s3_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 3: {int(entries[2].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s3_label.place(relx=42/1920, rely=0.675)
            Q1s3_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s3_assign.configure(command=lambda ns=num_sections: q1s3_assignment_setup(ns))
            Q1s3_assign.place(relx=503/1920, rely=0.675)
            q1_setup_items.append(Q1s1_label)
            q1_setup_items.append(Q1s1_assign)
            q1_setup_items.append(Q1s2_label)
            q1_setup_items.append(Q1s2_assign)
            q1_setup_items.append(Q1s3_label)
            q1_setup_items.append(Q1s3_assign)
        elif num_sections == 4:
            Q1s1 = Q1.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q1s2 = Q1.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q1s3 = Q1.add_section(section_percent=int(entries[2].get())/100 if entries[2].get()!="" else 0)
            Q1s4 = Q1.add_section(section_percent=int(entries[3].get())/100 if entries[3].get()!="" else 0)
            Q1_curr_sections.append(Q1s1)
            Q1_curr_sections.append(Q1s2)
            Q1_curr_sections.append(Q1s3)
            Q1_curr_sections.append(Q1s4)
            Q1s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s1_label.place(relx=42/1920, rely=0.07825)
            Q1s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s1_assign.configure(command=lambda ns=num_sections: q1s1_assignment_setup(ns))
            Q1s1_assign.place(relx=503/1920, rely=0.0785)
            Q1s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s2_label.place(relx=42/1920, rely=0.07825+1*(0.225))
            Q1s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s2_assign.configure(command=lambda ns=num_sections: q1s2_assignment_setup(ns))
            Q1s2_assign.place(relx=503/1920, rely=0.07825+1*(0.225))
            Q1s3_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 3: {int(entries[2].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s3_label.place(relx=42/1920, rely=0.07825+2*(0.225))
            Q1s3_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s3_assign.configure(command=lambda ns=num_sections: q1s3_assignment_setup(ns))
            Q1s3_assign.place(relx=503/1920, rely=0.07825+2*(0.225))
            Q1s4_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 4: {int(entries[3].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q1s4_label.place(relx=42/1920, rely=0.07825+3*(0.225))
            Q1s4_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q1s4_assign.configure(command=lambda ns=num_sections: q1s4_assignment_setup(ns))
            Q1s4_assign.place(relx=503/1920, rely=0.07825+3*(0.225))
            q1_setup_items.append(Q1s1_label)
            q1_setup_items.append(Q1s1_assign)
            q1_setup_items.append(Q1s2_label)
            q1_setup_items.append(Q1s2_assign)
            q1_setup_items.append(Q1s3_label)
            q1_setup_items.append(Q1s3_assign)
            q1_setup_items.append(Q1s4_label)
            q1_setup_items.append(Q1s4_assign)
    else:
        if num_sections == 2:
            Q2s1 = Q2.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q2s2 = Q2.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q2_curr_sections.append(Q2s1)
            Q2_curr_sections.append(Q2s2)
            Q2s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s1_label.place(relx=(42+670)/1920, rely=0.07825)
            Q2s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s1_assign.configure(command=lambda ns=num_sections: q2s1_assignment_setup(ns))
            Q2s1_assign.place(relx=(503+670)/1920, rely=0.0785)
            Q2s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s2_label.place(relx=(42+670)/1920, rely=0.5)
            Q2s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s2_assign.configure(command=lambda ns=num_sections: q2s2_assignment_setup(ns))
            Q2s2_assign.place(relx=(503+670)/1920, rely=0.5)            
            q2_setup_items.append(Q2s1_label)
            q2_setup_items.append(Q2s1_assign)
            q2_setup_items.append(Q2s2_label)
            q2_setup_items.append(Q2s2_assign)
        elif num_sections == 3:
            Q2s1 = Q2.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q2s2 = Q2.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q2s3 = Q2.add_section(section_percent=int(entries[2].get())/100 if entries[2].get()!="" else 0)
            Q2_curr_sections.append(Q2s1)
            Q2_curr_sections.append(Q2s2)
            Q2_curr_sections.append(Q2s3)
            Q2s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s1_label.place(relx=(42+670)/1920, rely=0.07825)
            Q2s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s1_assign.configure(command=lambda ns=num_sections: q2s1_assignment_setup(ns))
            Q2s1_assign.place(relx=(503+670)/1920, rely=0.0785)
            Q2s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s2_label.place(relx=(42+670)/1920, rely=0.375)
            Q2s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s2_assign.configure(command=lambda ns=num_sections: q2s2_assignment_setup(ns))
            Q2s2_assign.place(relx=(503+670)/1920, rely=0.375)
            Q2s3_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 3: {int(entries[2].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s3_label.place(relx=(42+670)/1920, rely=0.675)
            Q2s3_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s3_assign.configure(command=lambda ns=num_sections: q2s3_assignment_setup(ns))
            Q2s3_assign.place(relx=(503+670)/1920, rely=0.675)
            q2_setup_items.append(Q2s1_label)
            q2_setup_items.append(Q2s1_assign)
            q2_setup_items.append(Q2s2_label)
            q2_setup_items.append(Q2s2_assign)
            q2_setup_items.append(Q2s3_label)
            q2_setup_items.append(Q2s3_assign)
        elif num_sections == 4:
            Q2s1 = Q2.add_section(section_percent=int(entries[0].get())/100 if entries[0].get()!="" else 0)
            Q2s2 = Q2.add_section(section_percent=int(entries[1].get())/100 if entries[1].get()!="" else 0)
            Q2s3 = Q2.add_section(section_percent=int(entries[2].get())/100 if entries[2].get()!="" else 0)
            Q2s4 = Q2.add_section(section_percent=int(entries[3].get())/100 if entries[3].get()!="" else 0)
            Q2_curr_sections.append(Q2s1)
            Q2_curr_sections.append(Q2s2)
            Q2_curr_sections.append(Q2s3)
            Q2_curr_sections.append(Q2s4)
            Q2s1_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 1: {int(entries[0].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s1_label.place(relx=(42+670)/1920, rely=0.07825)
            Q2s1_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s1_assign.configure(command=lambda ns=num_sections: q2s1_assignment_setup(ns))
            Q2s1_assign.place(relx=(503+670)/1920, rely=0.0785)
            Q2s2_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 2: {int(entries[1].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s2_label.place(relx=(42+670)/1920, rely=0.07825+1*(0.225))
            Q2s2_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s2_assign.configure(command=lambda ns=num_sections: q2s2_assignment_setup(ns))
            Q2s2_assign.place(relx=(503+670)/1920, rely=0.07825+1*(0.225))
            Q2s3_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 3: {int(entries[2].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s3_label.place(relx=(42+670)/1920, rely=0.07825+2*(0.225))
            Q2s3_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s3_assign.configure(command=lambda ns=num_sections: q2s3_assignment_setup(ns))
            Q2s3_assign.place(relx=(503+670)/1920, rely=0.07825+2*(0.225))
            Q2s4_label = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text=f"Section 4: {int(entries[3].get())}%", fg="black", font=("Times New Roman", 28), relief="groove")
            Q2s4_label.place(relx=(42+670)/1920, rely=0.07825+3*(0.225))
            Q2s4_assign = tk.Button(width=int(12*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="green", fg="black", text="Assignment +", font=("Times New Roman", 18), relief="solid")
            Q2s4_assign.configure(command=lambda ns=num_sections: q2s4_assignment_setup(ns))
            Q2s4_assign.place(relx=(503+670)/1920, rely=0.07825+3*(0.225))
            print("bro what")
            q2_setup_items.append(Q2s1_label)
            q2_setup_items.append(Q2s1_assign)
            q2_setup_items.append(Q2s2_label)
            q2_setup_items.append(Q2s2_assign)
            q2_setup_items.append(Q2s3_label)
            q2_setup_items.append(Q2s3_assign)
            q2_setup_items.append(Q2s4_label)
            q2_setup_items.append(Q2s4_assign)
    for widget in percent_buttons:
        widget.destroy()
    print("Section creation successful")

def assignment_screen_setup(isQ1, num_sections):
    if isQ1:
        if num_sections <= 1:
            q1_assignment_button = tk.Button(width=int(17*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text="Add New Assignment", font=("Times New Roman", 40), relief="raised")
            q1_assignment_button.configure(command=lambda ns=num_sections: q1s1_assignment_setup(ns))
            q1_assignment_button.place(relx=95/1920, rely=930/1080)
            q1_setup_items.append(q1_assignment_button)
        else:
            q1percents_label = tk.Label(width=int(-150*WIDTH_MULTIPLIER), height=int(-80*HEIGHT_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 24), relief="solid", text="Pick Section Percents(MUST Add up to 100%)", justify="center")
            q1percents_label.place(relx=52.5/1920, rely=0.1)
            q1_percent_items.append(q1percents_label)
            q1validate_percents_button = tk.Button(width=int(-30*WIDTH_MULTIPLIER), bg="green", fg="black", font=("Times New Roman", 20), relief="solid", justify="center", text="Verify & Submit Sections")
            q1validate_percents_button.place(relx=115/1920, rely=0.9)
            q1_percent_items.append(q1validate_percents_button)
            if num_sections == 2:
                q1section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q1section1_label.place(relx=160/1920, rely=0.3)
                q1section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q1section2_label.place(relx=160/1920, rely=0.6)
                q1section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section1_entry.place(relx=425/1920, rely=0.3)
                q1section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section2_entry.place(relx=425/1920, rely=0.6)
                q1_percent_items.append(q1section1_label)
                q1_percent_items.append(q1section2_label)
                q1_percent_items.append(q1section1_entry)
                q1_percent_items.append(q1section2_entry)
                q1validate_percents_button.configure(command=lambda b=True, ns=2, pi=q1_percent_items, s1_p=q1section1_entry, s2_p=q1section2_entry:create_sections(b, ns, pi, s1_p, s2_p) if verify_percents(s1_p, s2_p) else print("Sections creation unsuccessful"))
            elif num_sections == 3:
                q1section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q1section1_label.place(relx=160/1920, rely=0.3)
                q1section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q1section2_label.place(relx=160/1920, rely=0.45)
                q1section3_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 3 %:", font=("Times New Roman", 32))
                q1section3_label.place(relx=160/1920, rely=0.6)
                q1section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section1_entry.place(relx=425/1920, rely=0.3)
                q1section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section2_entry.place(relx=425/1920, rely=0.45)
                q1section3_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section3_entry.place(relx=425/1920, rely=0.6)
                q1_percent_items.append(q1section1_label)
                q1_percent_items.append(q1section2_label)
                q1_percent_items.append(q1section3_label)
                q1_percent_items.append(q1section1_entry)
                q1_percent_items.append(q1section2_entry)
                q1_percent_items.append(q1section3_entry)
                q1validate_percents_button.configure(command=lambda b=True, ns=3, pi=q1_percent_items, s1_p=q1section1_entry, s2_p=q1section2_entry, s3_p=q1section3_entry:create_sections(b, ns, pi, s1_p, s2_p, s3_p) if verify_percents(s1_p, s2_p, s3_p) else print("Sections creation unsuccessful"))
            elif num_sections == 4:
                q1section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q1section1_label.place(relx=160/1920, rely=0.225)
                q1section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q1section2_label.place(relx=160/1920, rely=0.4)
                q1section3_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 3 %:", font=("Times New Roman", 32))
                q1section3_label.place(relx=160/1920, rely=0.575)
                q1section4_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 4 %:", font=("Times New Roman", 32))
                q1section4_label.place(relx=160/1920, rely=0.75)
                q1section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section1_entry.place(relx=425/1920, rely=0.225)
                q1section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section2_entry.place(relx=425/1920, rely=0.4)
                q1section3_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section3_entry.place(relx=425/1920, rely=0.575)
                q1section4_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q1section4_entry.place(relx=425/1920, rely=0.75)
                q1_percent_items.append(q1section1_label)
                q1_percent_items.append(q1section2_label)
                q1_percent_items.append(q1section3_label)
                q1_percent_items.append(q1section4_label)
                q1_percent_items.append(q1section1_entry)
                q1_percent_items.append(q1section2_entry)
                q1_percent_items.append(q1section3_entry)
                q1_percent_items.append(q1section4_entry)
                q1validate_percents_button.configure(command=lambda b=True, ns=4, pi=q1_percent_items, s1_p=q1section1_entry, s2_p=q1section2_entry, s3_p=q1section3_entry, s4_p=q1section4_entry:create_sections(b, ns, pi, s1_p, s2_p, s3_p, s4_p) if verify_percents(s1_p, s2_p, s3_p, s4_p) else print("Sections creation unsuccessful"))
        q1_back_button = tk.Button(width=int(5*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text="←", font=("Times New Roman", 19), relief="raised")
        q1_back_button.configure(command=lambda q=True, b=q1_back_button, setup=q1_setup_items, percent=q1_percent_items: reset_quarter(q, b, setup, percent))
        q1_back_button.place(relx=41.5/1920, rely=33/1080)
    else:
        if num_sections <= 1:
            q2_assignment_button = tk.Button(width=int(17*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text="Add New Assignment", font=("Times New Roman", 40), relief="raised")
            q2_assignment_button.configure(command=lambda ns=num_sections: q2s1_assignment_setup(ns))
            q2_assignment_button.place(relx=765/1920, rely=930/1080)
            q2_setup_items.append(q2_assignment_button)
        else:
            q2percents_label = tk.Label(width=int(-150*WIDTH_MULTIPLIER), height=int(-80*HEIGHT_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 24), relief="solid", text="Pick Section Percents(MUST Add up to 100%)", justify="center")
            q2percents_label.place(relx=(52.5+670)/1920, rely=0.1)
            q2_percent_items.append(q2percents_label)
            q2validate_percents_button = tk.Button(width=int(-30*WIDTH_MULTIPLIER), bg="green", fg="black", font=("Times New Roman", 20), relief="solid", justify="center", text="Verify & Submit Sections")
            q2validate_percents_button.place(relx=(115+670)/1920, rely=0.9)
            q2_percent_items.append(q2validate_percents_button)
            if num_sections == 2:
                q2section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q2section1_label.place(relx=(160+670)/1920, rely=0.3)
                q2section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q2section2_label.place(relx=(160+670)/1920, rely=0.6)
                q2section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section1_entry.place(relx=(425+670)/1920, rely=0.3)
                q2section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section2_entry.place(relx=(425+670)/1920, rely=0.6)
                q2_percent_items.append(q2section1_label)
                q2_percent_items.append(q2section2_label)
                q2_percent_items.append(q2section1_entry)
                q2_percent_items.append(q2section2_entry)
                q2validate_percents_button.configure(command=lambda b=False, ns=2, pi=q2_percent_items, s1_p=q2section1_entry, s2_p=q2section2_entry:create_sections(b, ns, pi, s1_p, s2_p) if verify_percents(s1_p, s2_p) else print("Sections creation unsuccessful"))
            elif num_sections == 3:
                q2section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q2section1_label.place(relx=(160+670)/1920, rely=0.3)
                q2section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q2section2_label.place(relx=(160+670)/1920, rely=0.45)
                q2section3_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 3 %:", font=("Times New Roman", 32))
                q2section3_label.place(relx=(160+670)/1920, rely=0.6)
                q2section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section1_entry.place(relx=(425+670)/1920, rely=0.3)
                q2section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section2_entry.place(relx=(425+670)/1920, rely=0.45)
                q2section3_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section3_entry.place(relx=(425+670)/1920, rely=0.6)
                q2_percent_items.append(q2section1_label)
                q2_percent_items.append(q2section2_label)
                q2_percent_items.append(q2section3_label)
                q2_percent_items.append(q2section1_entry)
                q2_percent_items.append(q2section2_entry)
                q2_percent_items.append(q2section3_entry)
                q2validate_percents_button.configure(command=lambda b=False, ns=3, pi=q2_percent_items, s1_p=q2section1_entry, s2_p=q2section2_entry, s3_p=q2section3_entry:create_sections(b, ns, pi, s1_p, s2_p, s3_p) if verify_percents(s1_p, s2_p, s3_p) else print("Sections creation unsuccessful"))
            elif num_sections == 4:
                q2section1_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 1 %:", font=("Times New Roman", 32))
                q2section1_label.place(relx=(160+670)/1920, rely=0.225)
                q2section2_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 2 %:", font=("Times New Roman", 32))
                q2section2_label.place(relx=(160+670)/1920, rely=0.4)
                q2section3_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 3 %:", font=("Times New Roman", 32))
                q2section3_label.place(relx=(160+670)/1920, rely=0.575)
                q2section4_label = tk.Label(width=int(-40*WIDTH_MULTIPLIER), height=int(-40*HEIGHT_MULTIPLIER), bg="white", fg="black", justify="center", relief="raised", text="Section 4 %:", font=("Times New Roman", 32))
                q2section4_label.place(relx=(160+670)/1920, rely=0.75)
                q2section1_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section1_entry.place(relx=(425+670)/1920, rely=0.225)
                q2section2_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section2_entry.place(relx=(425+670)/1920, rely=0.4)
                q2section3_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section3_entry.place(relx=(425+670)/1920, rely=0.575)
                q2section4_entry = tk.Entry(width=int(-40*WIDTH_MULTIPLIER), bg="white", fg="black", justify="center", relief="solid", font=("Times New Roman", 32))
                q2section4_entry.place(relx=(425+670)/1920, rely=0.75)
                q2_percent_items.append(q2section1_label)
                q2_percent_items.append(q2section2_label)
                q2_percent_items.append(q2section3_label)
                q2_percent_items.append(q2section4_label)
                q2_percent_items.append(q2section1_entry)
                q2_percent_items.append(q2section2_entry)
                q2_percent_items.append(q2section3_entry)
                q2_percent_items.append(q2section4_entry)
                q2validate_percents_button.configure(command=lambda b=False, ns=4, pi=q2_percent_items, s1_p=q2section1_entry, s2_p=q2section2_entry, s3_p=q2section3_entry, s4_p=q2section4_entry:create_sections(b, ns, pi, s1_p, s2_p, s3_p, s4_p) if verify_percents(s1_p, s2_p, s3_p, s4_p) else print("Sections creation unsuccessful"))
        q2_back_button = tk.Button(width=int(5*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", fg="black", text="←", font=("Times New Roman", 19), relief="raised")
        q2_back_button.configure(command=lambda q=False, b=q2_back_button, setup=q2_setup_items, percent=q2_percent_items: reset_quarter(q, b, setup, percent))
        q2_back_button.place(relx=(2*(40.75/1920)+(630/1920)), rely=33/1080)

def reset_quarter(isQ1, back_button, setup_items, percent_items):
    global q1s1_assignment_function_calls
    global q1s2_assignment_function_calls
    global q1s3_assignment_function_calls
    global q1s4_assignment_function_calls
    global q2s1_assignment_function_calls
    global q2s2_assignment_function_calls
    global q2s3_assignment_function_calls
    global q2s4_assignment_function_calls
    if isQ1:
        back_button.destroy()
        for widget in setup_items:
            widget.destroy()
        for widget in percent_items:
            widget.destroy()
        q1s1_assignment_function_calls = 0
        q1s2_assignment_function_calls = 0
        q1s3_assignment_function_calls = 0
        q1s4_assignment_function_calls = 0
        q1_one_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="1 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q1_one_section_button.place(relx=0.09, rely=0.1625)
        q1_two_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="2 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q1_two_section_button.place(relx=0.09, rely=0.3625)
        q1_three_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="3 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q1_three_section_button.place(relx=0.09, rely=0.5625)
        q1_four_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="4 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q1_four_section_button.place(relx=0.09, rely=0.7625)
        q1_section_buttons = [q1_one_section_button, q1_two_section_button, q1_three_section_button, q1_four_section_button]
        q1_one_section_button.config(command=lambda b=q1_section_buttons: q1_one_sections(b))
        q1_two_section_button.config(command=lambda b=q1_section_buttons: q1_two_sections(b))
        q1_three_section_button.config(command=lambda b=q1_section_buttons: q1_three_sections(b))
        q1_four_section_button.config(command=lambda b=q1_section_buttons: q1_four_sections(b))
        clear_sections(isQ1)
    else:
        back_button.destroy()
        for widget in setup_items:
            widget.destroy()
        for widget in percent_items:
            widget.destroy()
        q2s1_assignment_function_calls = 0
        q2s2_assignment_function_calls = 0
        q2s3_assignment_function_calls = 0
        q2s4_assignment_function_calls = 0
        q2_one_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="1 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q2_one_section_button.place(relx=0.439, rely=0.1625)
        q2_two_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="2 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q2_two_section_button.place(relx=0.439, rely=0.3625)
        q2_three_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="3 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q2_three_section_button.place(relx=0.439, rely=0.5625)
        q2_four_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="4 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
        q2_four_section_button.place(relx=0.439, rely=0.7625)
        q2_section_buttons = [q2_one_section_button, q2_two_section_button, q2_three_section_button, q2_four_section_button]
        q2_one_section_button.config(command=lambda b=q2_section_buttons: q2_one_sections(b))
        q2_two_section_button.config(command=lambda b=q2_section_buttons: q2_two_sections(b))
        q2_three_section_button.config(command=lambda b=q2_section_buttons: q2_three_sections(b))
        q2_four_section_button.config(command=lambda b=q2_section_buttons: q2_four_sections(b))
        clear_sections(isQ1)

def q1_one_sections(section_buttons):
    global Q1s1
    Q1s1 = Q1.add_section(section_percent=1)
    Q1_curr_sections.append(Q1s1)
    clear_section_buttons(section_buttons)
    assignment_screen_setup(True,1)

def q1_two_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(True,2)

def q1_three_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(True,3)

def q1_four_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(True,4)

def q2_one_sections(section_buttons):
    global Q2s1
    Q2s1 = Q2.add_section(section_percent=1)
    Q2_curr_sections.append(Q2s1)
    clear_section_buttons(section_buttons)
    assignment_screen_setup(False,1)

def q2_two_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(False,2)

def q2_three_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(False,3)

def q2_four_sections(section_buttons):
    clear_section_buttons(section_buttons)
    assignment_screen_setup(False,4)

def update_midterm():
    try:
        M1.grade = int(Exam_grade.get())
    except:
        pass
    window.after(50, update_midterm)

def update_assign_grades(current_sections):
    if current_sections == []:
        return
    for section in current_sections:
        for assignment in section.assignments:
            assignment.update_grade()
    window.after(50, update_assign_grades(current_sections))

def q1_calculate_score():
    try:
        quarter_grade = Q1.get_quarter_grade()
    except:
        quarter_grade = 0
    q1_grade.set(quarter_grade)
    window.after(50, q1_calculate_score)

def q2_calculate_score():
    try:
        quarter_grade = Q2.get_quarter_grade()
    except:
        quarter_grade = 0
    q2_grade.set(quarter_grade)
    window.after(50, q2_calculate_score)

def final_calculate_score():
    try:
        f_Grade = total_grade.get_final_grade()
    except:
        f_Grade = 0
    final_grade.set(f_Grade)
    window.after(50, final_calculate_score)


Q1_area = tk.Frame(width=int(630*WIDTH_MULTIPLIER), height=int(1020*HEIGHT_MULTIPLIER), highlightbackground="black", highlightthickness=2, bg="white")
Q1_area.place(relx=40/1920, rely=30/1080)
Q1_title = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Q1 (40%)", fg="black", font=("Times New Roman", 32), relief="solid")
Q1_title.place(relx=40/1920, rely=30/1080)
Q2_area = tk.Frame(width=int(630*WIDTH_MULTIPLIER), height=int(1020*HEIGHT_MULTIPLIER), highlightbackground="black", highlightthickness=2, bg="white")
Q2_area.place(relx=(2*(40/1920)+(630/1920)), rely=30/1080)
Q2_title = tk.Label(width=int(26*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Q2 (40%)", fg="black", font=("Times New Roman", 32), relief="solid")
Q2_title.place(relx=(2*(40/1920)+(630/1920)), rely=30/1080)
Exam_area = tk.Frame(width=int(500*WIDTH_MULTIPLIER), height=int(495*HEIGHT_MULTIPLIER), highlightbackground="black", highlightthickness=2, bg="white")
Exam_area.place(relx=(3*(40/1920)+(2*(630/1920))), rely=30/1080)
Exam_title = tk.Label(width=int(19*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Midterm (20%)", fg="black", font=("Times New Roman", 35), relief="solid")
Exam_title.place(relx=(3*(40/1920)+(2*(630/1920))), rely=30/1080)
Exam_grade = tk.Entry(width=int(10*WIDTH_MULTIPLIER), bg="white", fg="black", font=("Times New Roman", 73), relief="sunken", justify="center", highlightbackground="black", highlightthickness=1)
Exam_grade.bind("<FocusIn>", lambda event, e=Exam_grade: on_entry_click(event, e))
Exam_grade.bind("<FocusOut>", lambda event, e=Exam_grade: on_entry_leave(event, e))
Exam_grade.place(relx=(3.05*(40/1920)+(2*(630/1920))), rely=220/1080)
Grades_area = tk.Frame(width=int(500*WIDTH_MULTIPLIER), height=int(495*HEIGHT_MULTIPLIER), highlightbackground="black", highlightthickness=2, bg="white")
Grades_area.place(relx=(3*(40/1920)+(2*(630/1920))), rely=(2*(30/1080)+(495/1080)))
Q1_grade_label = tk.Label(width=int(10*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Q1 Grade", fg="black", font=("Times New Roman", 34), relief="solid")
Q1_grade_label.place(relx=(3*(40/1920)+(2*(630/1920))), rely=(2*(30/1080)+(495/1080)))
Q1_grade_score = tk.Label(width=int(4*WIDTH_MULTIPLIER), height=int(2*HEIGHT_MULTIPLIER), bg="white", textvariable=q1_grade, fg="black", font=("Times New Roman", 67))
Q1_grade_score.place(relx=(3*(47/1920)+(2*(630/1920))), rely=(3.85*(30/1080)+(495/1080)))
Q2_grade_label = tk.Label(width=int(10*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Q2 Grade", fg="black", font=("Times New Roman", 34), relief="solid")
Q2_grade_label.place(relx=(9.1*(40/1920)+(2*(630/1920))), rely=(2*(30/1080)+(495/1080)))
Q2_grade_score = tk.Label(width=int(5*WIDTH_MULTIPLIER), height=int(2*HEIGHT_MULTIPLIER), bg="white", textvariable=q2_grade, fg="black", font=("Times New Roman", 67))
Q2_grade_score.place(relx=(9*(40/1920)+(2*(630/1920))), rely=(3.85*(30/1080)+(495/1080)))
Final_grade_score = tk.Label(width=int(10*WIDTH_MULTIPLIER), height=int(2*HEIGHT_MULTIPLIER), bg="white", textvariable=final_grade, fg="black", font=("Times New Roman", 60))
Final_grade_score.place(relx=(3*(40/1920)+(2.025*(630/1920))), rely=(3*(30/1080)+1.557*(495/1080)))
Final_grade_label = tk.Label(width=int(19*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="Final Grade", fg="black", font=("Times New Roman", 35), relief="solid")
Final_grade_label.place(relx=(3*(40/1920)+(2*(630/1920))), rely=(2*(30/1080)+1.5*(495/1080)))

q1_one_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="1 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q1_one_section_button.place(relx=0.09, rely=0.1625)
q1_two_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="2 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q1_two_section_button.place(relx=0.09, rely=0.3625)
q1_three_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="3 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q1_three_section_button.place(relx=0.09, rely=0.5625)
q1_four_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="4 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q1_four_section_button.place(relx=0.09, rely=0.7625)
q2_one_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="1 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q2_one_section_button.place(relx=0.439, rely=0.1625)
q2_two_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="2 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q2_two_section_button.place(relx=0.439, rely=0.3625)
q2_three_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="3 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q2_three_section_button.place(relx=0.439, rely=0.5625)
q2_four_section_button = tk.Button(width=int(15*WIDTH_MULTIPLIER), height=int(1*HEIGHT_MULTIPLIER), bg="white", text="4 Section Quarter", fg="black", font=("Times New Roman", 33), relief="raised")
q2_four_section_button.place(relx=0.439, rely=0.7625)
q1_section_buttons = [q1_one_section_button, q1_two_section_button, q1_three_section_button, q1_four_section_button]
q2_section_buttons = [q2_one_section_button, q2_two_section_button, q2_three_section_button, q2_four_section_button]
q1_one_section_button.config(command=lambda b=q1_section_buttons: q1_one_sections(b))
q1_two_section_button.config(command=lambda b=q1_section_buttons: q1_two_sections(b))
q1_three_section_button.config(command=lambda b=q1_section_buttons: q1_three_sections(b))
q1_four_section_button.config(command=lambda b=q1_section_buttons: q1_four_sections(b))
q2_one_section_button.config(command=lambda b=q2_section_buttons: q2_one_sections(b))
q2_two_section_button.config(command=lambda b=q2_section_buttons: q2_two_sections(b))
q2_three_section_button.config(command=lambda b=q2_section_buttons: q2_three_sections(b))
q2_four_section_button.config(command=lambda b=q2_section_buttons: q2_four_sections(b))


window.after(50, update_midterm)
window.after(50, q1_calculate_score)
window.after(50, q2_calculate_score)
window.after(50, final_calculate_score)
window.after(50, update_assign_grades(Q1_curr_sections))
window.after(50, update_assign_grades(Q2_curr_sections))

window.mainloop()