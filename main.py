import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

APP_TITLE = "Smart Care - Hospital Management System"
DB_NAME = "smart_care_hospital.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def initialize_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT,
                address TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                phone TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                reason TEXT,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                payment_status TEXT NOT NULL DEFAULT 'Unpaid',
                created_at TEXT NOT NULL,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            )
        """)


class SmartCareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1080x700")
        self.minsize(920, 600)
        self.configure(padx=14, pady=14)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Treeview", rowheight=27)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="SMART CARE", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Hospital Management System  |  Patients • Doctors • Appointments • Billing",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        self.patient_tab = ttk.Frame(self.tabs, padding=10)
        self.doctor_tab = ttk.Frame(self.tabs, padding=10)
        self.appointment_tab = ttk.Frame(self.tabs, padding=10)
        self.bill_tab = ttk.Frame(self.tabs, padding=10)
        self.tabs.add(self.patient_tab, text="Patients")
        self.tabs.add(self.doctor_tab, text="Doctors")
        self.tabs.add(self.appointment_tab, text="Appointments")
        self.tabs.add(self.bill_tab, text="Billing")

        self.build_patients()
        self.build_doctors()
        self.build_appointments()
        self.build_bills()
        self.refresh_all()

    def make_tree(self, parent, columns, headings, widths):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=(10, 0))
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        return tree

    def build_patients(self):
        form = ttk.LabelFrame(self.patient_tab, text="Register patient", padding=10)
        form.pack(fill="x")
        self.p_name = tk.StringVar()
        self.p_age = tk.StringVar()
        self.p_gender = tk.StringVar(value="Other")
        self.p_phone = tk.StringVar()
        self.p_address = tk.StringVar()
        for label, var, row, col in [
            ("Name*", self.p_name, 0, 0), ("Age*", self.p_age, 0, 2),
            ("Phone", self.p_phone, 1, 0), ("Address", self.p_address, 1, 2)
        ]:
            ttk.Label(form, text=label).grid(row=row, column=col, sticky="w", padx=5, pady=5)
            ttk.Entry(form, textvariable=var, width=27).grid(row=row, column=col + 1, sticky="ew", padx=5, pady=5)
        ttk.Label(form, text="Gender").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.p_gender, values=["Female", "Male", "Other"],
                     state="readonly", width=12).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(form, text="Add patient", command=self.add_patient).grid(row=1, column=4, padx=5, pady=5)
        ttk.Button(form, text="Clear", command=self.clear_patient_form).grid(row=1, column=5, padx=5, pady=5)
        self.patient_tree = self.make_tree(
            self.patient_tab, ("id", "name", "age", "gender", "phone", "address"),
            ("ID", "Name", "Age", "Gender", "Phone", "Address"), (55, 180, 55, 90, 130, 300))
        ttk.Button(self.patient_tab, text="Delete selected patient", command=self.delete_patient).pack(anchor="e", pady=8)

    def build_doctors(self):
        form = ttk.LabelFrame(self.doctor_tab, text="Register doctor", padding=10)
        form.pack(fill="x")
        self.d_name, self.d_department, self.d_phone = tk.StringVar(), tk.StringVar(), tk.StringVar()
        for label, var, col in [("Name*", self.d_name, 0), ("Department*", self.d_department, 2), ("Phone", self.d_phone, 4)]:
            ttk.Label(form, text=label).grid(row=0, column=col, padx=5, pady=5, sticky="w")
            ttk.Entry(form, textvariable=var, width=24).grid(row=0, column=col + 1, padx=5, pady=5)
        ttk.Button(form, text="Add doctor", command=self.add_doctor).grid(row=0, column=6, padx=5)
        self.doctor_tree = self.make_tree(
            self.doctor_tab, ("id", "name", "department", "phone"),
            ("ID", "Name", "Department", "Phone"), (60, 250, 230, 170))
        ttk.Button(self.doctor_tab, text="Delete selected doctor", command=self.delete_doctor).pack(anchor="e", pady=8)

    def build_appointments(self):
        form = ttk.LabelFrame(self.appointment_tab, text="Schedule appointment", padding=10)
        form.pack(fill="x")
        self.a_patient, self.a_doctor = tk.StringVar(), tk.StringVar()
        self.a_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.a_reason = tk.StringVar()
        ttk.Label(form, text="Patient*").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_combo = ttk.Combobox(form, textvariable=self.a_patient, state="readonly", width=27)
        self.patient_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Doctor*").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.doctor_combo = ttk.Combobox(form, textvariable=self.a_doctor, state="readonly", width=27)
        self.doctor_combo.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(form, text="Date/time*").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.a_date, width=29).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form, text="Reason").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.a_reason, width=29).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(form, text="Schedule", command=self.add_appointment).grid(row=0, column=4, rowspan=2, padx=8)
        ttk.Label(form, text="Date format: YYYY-MM-DD HH:MM").grid(row=2, column=0, columnspan=3, sticky="w", padx=5)
        self.appointment_tree = self.make_tree(
            self.appointment_tab, ("id", "patient", "doctor", "date", "reason", "status"),
            ("ID", "Patient", "Doctor", "Date/time", "Reason", "Status"), (50, 170, 170, 155, 250, 100))
        ttk.Button(self.appointment_tab, text="Mark selected as completed",
                   command=self.complete_appointment).pack(anchor="e", pady=8)

    def build_bills(self):
        form = ttk.LabelFrame(self.bill_tab, text="Create bill", padding=10)
        form.pack(fill="x")
        self.b_patient, self.b_amount, self.b_description = tk.StringVar(), tk.StringVar(), tk.StringVar()
        ttk.Label(form, text="Patient*").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.bill_patient_combo = ttk.Combobox(form, textvariable=self.b_patient, state="readonly", width=27)
        self.bill_patient_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Amount (₹)*").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.b_amount, width=18).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(form, text="Description").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.b_description, width=60).grid(
            row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        ttk.Button(form, text="Create unpaid bill", command=self.add_bill).grid(row=0, column=4, rowspan=2, padx=8)
        self.bill_tree = self.make_tree(
            self.bill_tab, ("id", "patient", "amount", "description", "status", "created"),
            ("Bill ID", "Patient", "Amount (₹)", "Description", "Payment status", "Created"),
            (65, 180, 110, 260, 130, 160))
        ttk.Button(self.bill_tab, text="Mark selected as paid", command=self.pay_bill).pack(anchor="e", pady=8)

    def add_patient(self):
        name, age_text = self.p_name.get().strip(), self.p_age.get().strip()
        if not name or not age_text:
            messagebox.showwarning("Missing details", "Patient name and age are required.")
            return
        try:
            age = int(age_text)
            if not 0 <= age <= 130:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid age", "Enter an age between 0 and 130.")
            return
        with connect_db() as con:
            con.execute("INSERT INTO patients(name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
                        (name, age, self.p_gender.get(), self.p_phone.get().strip(), self.p_address.get().strip()))
        self.clear_patient_form()
        self.refresh_all()
        messagebox.showinfo("Smart Care", "Patient registered successfully.")

    def clear_patient_form(self):
        for var in (self.p_name, self.p_age, self.p_phone, self.p_address):
            var.set("")
        self.p_gender.set("Other")

    def delete_patient(self):
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Select patient", "Select a patient to delete.")
            return
        patient_id = self.patient_tree.item(selected[0], "values")[0]
        with connect_db() as con:
            related = con.execute(
                "SELECT (SELECT COUNT(*) FROM appointments WHERE patient_id=?) + "
                "(SELECT COUNT(*) FROM bills WHERE patient_id=?)", (patient_id, patient_id)).fetchone()[0]
            if related:
                messagebox.showerror("Cannot delete", "This patient has appointments or bills; keep the record for history.")
                return
            con.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        self.refresh_all()

    def add_doctor(self):
        name, dept = self.d_name.get().strip(), self.d_department.get().strip()
        if not name or not dept:
            messagebox.showwarning("Missing details", "Doctor name and department are required.")
            return
        with connect_db() as con:
            con.execute("INSERT INTO doctors(name, department, phone) VALUES (?, ?, ?)",
                        (name, dept, self.d_phone.get().strip()))
        self.d_name.set(""); self.d_department.set(""); self.d_phone.set("")
        self.refresh_all()
        messagebox.showinfo("Smart Care", "Doctor added successfully.")

    def delete_doctor(self):
        selected = self.doctor_tree.selection()
        if not selected:
            messagebox.showwarning("Select doctor", "Select a doctor to delete.")
            return
        doctor_id = self.doctor_tree.item(selected[0], "values")[0]
        with connect_db() as con:
            if con.execute("SELECT COUNT(*) FROM appointments WHERE doctor_id=?", (doctor_id,)).fetchone()[0]:
                messagebox.showerror("Cannot delete", "This doctor has appointments; keep the record for history.")
                return
            con.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
        self.refresh_all()

    def add_appointment(self):
        if not self.a_patient.get() or not self.a_doctor.get() or not self.a_date.get().strip():
            messagebox.showwarning("Missing details", "Choose a patient, doctor, and date/time.")
            return
        date_text = self.a_date.get().strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid date", "Use YYYY-MM-DD HH:MM, e.g. 2026-10-20 14:30.")
            return
        patient_id = int(self.a_patient.get().split(" - ", 1)[0])
        doctor_id = int(self.a_doctor.get().split(" - ", 1)[0])
        with connect_db() as con:
            con.execute("INSERT INTO appointments(patient_id, doctor_id, appointment_date, reason) VALUES (?, ?, ?, ?)",
                        (patient_id, doctor_id, date_text, self.a_reason.get().strip()))
        self.a_reason.set("")
        self.refresh_all()
        messagebox.showinfo("Smart Care", "Appointment scheduled successfully.")

    def complete_appointment(self):
        selected = self.appointment_tree.selection()
        if not selected:
            messagebox.showwarning("Select appointment", "Select an appointment first.")
            return
        appointment_id = self.appointment_tree.item(selected[0], "values")[0]
        with connect_db() as con:
            con.execute("UPDATE appointments SET status='Completed' WHERE id=?", (appointment_id,))
        self.refresh_all()

    def add_bill(self):
        if not self.b_patient.get() or not self.b_amount.get().strip():
            messagebox.showwarning("Missing details", "Choose a patient and enter an amount.")
            return
        try:
            amount = float(self.b_amount.get().strip())
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid amount", "Enter a non-negative number.")
            return
        patient_id = int(self.b_patient.get().split(" - ", 1)[0])
        with connect_db() as con:
            con.execute("INSERT INTO bills(patient_id, amount, description, created_at) VALUES (?, ?, ?, ?)",
                        (patient_id, amount, self.b_description.get().strip(),
                         datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.b_amount.set(""); self.b_description.set("")
        self.refresh_all()
        messagebox.showinfo("Smart Care", "Bill created successfully.")

    def pay_bill(self):
        selected = self.bill_tree.selection()
        if not selected:
            messagebox.showwarning("Select bill", "Select a bill first.")
            return
        bill_id = self.bill_tree.item(selected[0], "values")[0]
        with connect_db() as con:
            con.execute("UPDATE bills SET payment_status='Paid' WHERE id=?", (bill_id,))
        self.refresh_all()

    def refresh_all(self):
        with connect_db() as con:
            patients = con.execute("SELECT id, name, age, gender, phone, address FROM patients ORDER BY id DESC").fetchall()
            doctors = con.execute("SELECT id, name, department, phone FROM doctors ORDER BY id DESC").fetchall()
            appointments = con.execute("""
                SELECT a.id, p.name, d.name, a.appointment_date, a.reason, a.status
                FROM appointments a JOIN patients p ON p.id=a.patient_id
                JOIN doctors d ON d.id=a.doctor_id ORDER BY a.appointment_date DESC
            """).fetchall()
            bills = con.execute("""
                SELECT b.id, p.name, b.amount, b.description, b.payment_status, b.created_at
                FROM bills b JOIN patients p ON p.id=b.patient_id ORDER BY b.id DESC
            """).fetchall()
            patient_options = [f"{r[0]} - {r[1]}" for r in con.execute("SELECT id, name FROM patients ORDER BY name").fetchall()]
            doctor_options = [f"{r[0]} - {r[1]} ({r[2]})" for r in con.execute("SELECT id, name, department FROM doctors ORDER BY name").fetchall()]

        for tree, rows in [(self.patient_tree, patients), (self.doctor_tree, doctors),
                           (self.appointment_tree, appointments), (self.bill_tree, bills)]:
            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert("", "end", values=row)
        self.patient_combo["values"] = patient_options
        self.bill_patient_combo["values"] = patient_options
        self.doctor_combo["values"] = doctor_options


if __name__ == "__main__":
    initialize_db()
    SmartCareApp().mainloop()
