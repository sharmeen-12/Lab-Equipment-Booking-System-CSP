import tkinter as tk
from tkinter import messagebox

class LabBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Equipment Booking System")
        self.root.geometry("560x600")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        # Pre-loaded schedule database with student records
        self.bookings = {
            "Microscope A": [(9, 11), (14, 15)],
            "Spectrophotometer": [(11, 13)],
            "Centrifuge B": [],
            "3D Bioprinter": [(10, 12)]
        }
        
        self.setup_ui()
        self.load_initial_records()

    def setup_ui(self):
        # Main container with layout margins
        main_frame = tk.Frame(self.root, bg="#f5f6fa")
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Header Title
        title_label = tk.Label(main_frame, text="Lab Equipment Scheduler (CSP)", 
                               font=("Segoe UI", 16, "bold"), fg="#2c3e50", bg="#f5f6fa")
        title_label.pack(pady=(0, 15))

        # Input Container Frame
        form_frame = tk.LabelFrame(main_frame, text=" New Booking Request ", 
                                   font=("Segoe UI", 10, "bold"), fg="#34495e", bg="#f5f6fa", bd=1, relief="solid")
        form_frame.pack(fill="x", pady=(0, 15), ipady=10)
        form_frame.columnconfigure(1, weight=1)

        # 1. Equipment Selection Row (Radio Buttons)
        tk.Label(form_frame, text="Select Equipment:", font=("Segoe UI", 10, "bold"), bg="#f5f6fa").grid(row=0, column=0, sticky="nw", padx=15, pady=8)
        
        self.equip_var = tk.StringVar(value="Microscope A")
        radio_frame = tk.Frame(form_frame, bg="#f5f6fa")
        radio_frame.grid(row=0, column=1, padx=(0, 15), pady=8, sticky="w")

        equipment_list = list(self.bookings.keys())
        for index, equip in enumerate(equipment_list):
            tk.Radiobutton(radio_frame, text=equip, variable=self.equip_var, value=equip, 
                           bg="#f5f6fa", font=("Segoe UI", 10), activebackground="#f5f6fa").grid(row=index//2, column=index%2, sticky="w", padx=5, pady=2)

        # 2. Student Name Row
        tk.Label(form_frame, text="Student Name:", font=("Segoe UI", 10), bg="#f5f6fa").grid(row=1, column=0, sticky="w", padx=15, pady=8)
        self.name_entry = tk.Entry(form_frame, font=("Segoe UI", 10), bd=1, relief="solid")
        self.name_entry.grid(row=1, column=1, padx=(0, 15), pady=8, sticky="ew")

        # 3. Start Time Row (Vertical Fix)
        tk.Label(form_frame, text="Start Hour (9-16):", font=("Segoe UI", 10), bg="#f5f6fa").grid(row=2, column=0, sticky="w", padx=15, pady=8)
        self.start_entry = tk.Entry(form_frame, font=("Segoe UI", 10), bd=1, relief="solid")
        self.start_entry.grid(row=2, column=1, padx=(0, 15), pady=8, sticky="ew")

        # 4. End Time Row (Vertical Fix)
        tk.Label(form_frame, text="End Hour (10-17):", font=("Segoe UI", 10), bg="#f5f6fa").grid(row=3, column=0, sticky="w", padx=15, pady=8)
        self.end_entry = tk.Entry(form_frame, font=("Segoe UI", 10), bd=1, relief="solid")
        self.end_entry.grid(row=3, column=1, padx=(0, 15), pady=8, sticky="ew")

        # Verification Submission Trigger Button
        self.book_btn = tk.Button(main_frame, text="Verify & Book Slots", bg="#27ae60", fg="white", 
                                  font=("Segoe UI", 10, "bold"), activebackground="#219653", 
                                  activeforeground="white", bd=0, cursor="hand2", command=self.handle_booking)
        self.book_btn.pack(fill="x", ipady=8, pady=(0, 15))

        # View Log Frame
        list_frame = tk.Frame(main_frame, bg="#f5f6fa")
        list_frame.pack(fill="both", expand=True, pady=(15, 0))

        tk.Label(list_frame, text="Active Schedules Log:", font=("Segoe UI", 11, "bold"), fg="#2c3e50", bg="#f5f6fa").pack(anchor="w", pady=(0, 5))
        
        # Scrolled Listbox structure
        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side="right", fill="y")
        
        self.schedule_list = tk.Listbox(list_frame, font=("Consolas", 10), bd=1, relief="solid", yscrollcommand=scroll.set)
        self.schedule_list.pack(fill="both", expand=True)
        scroll.config(command=self.schedule_list.yview)

    def load_initial_records(self):
        # Initial display data populate
        records = [
            ("Ali Ahmed", "Microscope A", 9, 11),
            ("Zainab Khan", "Microscope A", 14, 15),
            ("Bilal Shah", "Spectrophotometer", 11, 13),
            ("Hamza Tariq", "3D Bioprinter", 10, 12)
        ]
        for name, equip, start, end in records:
            self.schedule_list.insert(tk.END, f" {name:<15} | {equip:<20} | {start:02d}:00 - {end:02d}:00")

    def check_csp_constraints(self, equipment, start, end):
        # Operational Constraints Validation (Lab Hours 9 to 17)
        if start < 9 or end > 17:
            return False, "Lab Operational Constraints: Standard hours are 09:00 to 17:00."
        
        # Timeline sequence evaluation
        if start >= end:
            return False, "Logic Constraint: End time must occur after the start time."
        
        # Fair booking duration allocation validation
        if (end - start) > 2:
            return False, "Fairness Policy Constraint: Maximum allocation limit is 2 hours."

        # Resource allocation overlap validation (Time Conflict Checking)
        for booked_start, booked_end in self.bookings[equipment]:
            if not (end <= booked_start or start >= booked_end):
                return False, f"Resource Conflict: Slot overlaps with an existing booking ({booked_start}:00 - {booked_end}:00)."
        
        return True, "Success"

    def handle_booking(self):
        student_name = self.name_entry.get().strip()
        equipment = self.equip_var.get()

        if not student_name:
            messagebox.showerror("Validation Error", "Student name field cannot be empty.")
            return

        try:
            start_time = int(self.start_entry.get())
            end_time = int(self.end_entry.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Timings must be valid integers (e.g., 9, 13).")
            return

        # Execute Constraint Satisfaction evaluation
        is_valid, message = self.check_csp_constraints(equipment, start_time, end_time)

        if is_valid:
            self.bookings[equipment].append((start_time, end_time))
            log_entry = f" {student_name:<15} | {equipment:<20} | {start_time:02d}:00 - {end_time:02d}:00"
            self.schedule_list.insert(tk.END, log_entry)
            
            # Input clean up
            self.name_entry.delete(0, tk.END)
            self.start_entry.delete(0, tk.END)
            self.end_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", f"Slot successfully allocated for {equipment}.")
        else:
            messagebox.showerror("Constraint Violation", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = LabBookingApp(root)
    root.mainloop()