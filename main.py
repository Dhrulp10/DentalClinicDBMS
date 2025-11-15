import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime

class DentalClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental Clinic Management System - Local SQLite")
        self.root.geometry("900x700")
        
        # SQLite database connection
        self.connection = None
        self.cursor = None
        self.db_file = "dental_clinic.db"
        
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_styles()
        
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.main_menu_frame = ttk.Frame(self.main_container)
        self.query_frame = ttk.Frame(self.main_container)
        self.schema_frame = ttk.Frame(self.main_container)
        
        self.setup_main_menu_frame()
        self.setup_query_frame()
        self.setup_schema_frame()
        
        # Auto-connect to SQLite database
        self.connect_to_sqlite()
        self.show_frame(self.main_menu_frame)
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
    
    def show_frame(self, frame):
        for f in [self.main_menu_frame, self.query_frame, self.schema_frame]:
            f.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)
    
    def connect_to_sqlite(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            print(f"Connected to SQLite database: {self.db_file}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Cannot connect to database: {str(e)}")
    
    def setup_main_menu_frame(self):
        title_label = ttk.Label(self.main_menu_frame, text="Dental Clinic Management System", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle = ttk.Label(self.main_menu_frame, text="Using Local SQLite Database",
                           font=('Arial', 10, 'italic'))
        subtitle.pack(pady=5)
        
        buttons = [
            ("🗑️ Drop All Tables", self.drop_tables),
            ("📊 Create Tables", self.create_tables),
            ("📥 Populate Tables", self.populate_tables),
            ("🔍 Run Queries", lambda: self.show_frame(self.query_frame)),
            ("📋 View Schema", self.show_schema),
            ("⚡ Interactive SQL", self.interactive_sql),
            ("🚪 Exit", self.exit_app)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.main_menu_frame, text=text, command=command)
            btn.pack(fill=tk.X, padx=50, pady=8)
        
        self.menu_status = ttk.Label(self.main_menu_frame, text="", style='Success.TLabel')
        self.menu_status.pack(pady=10)
    
    def setup_query_frame(self):
        header_frame = ttk.Frame(self.query_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(header_frame, text="← Back to Main Menu", 
                  command=lambda: self.show_frame(self.main_menu_frame)).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(header_frame, text="Predefined Queries", style='Title.TLabel').pack(side=tk.LEFT, padx=20)
        
        query_frame = ttk.Frame(self.query_frame)
        query_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(query_frame, text="Select Query:", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        self.query_var = tk.StringVar()
        queries = [
            ("Least Popular Treatments", "least_popular_treatments"),
            ("Patients with Both Treatments & Prescriptions", "patients_both"),
            ("Patients with Appointments but No Bills", "patients_no_bills"),
            ("Most Expensive Dental Actions", "most_expensive"),
            ("Patients with Appointments but No Treatments", "patients_no_treatments"),
            ("Patient Billing Summary", "billing_summary")
        ]
        
        query_combo = ttk.Combobox(query_frame, textvariable=self.query_var, 
                                  values=[q[0] for q in queries], state="readonly", width=40)
        query_combo.pack(side=tk.LEFT, padx=10)
        query_combo.set("Select a query...")
        
        ttk.Button(query_frame, text="Run Query", command=self.run_predefined_query).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(self.query_frame, text="Results:", style='Header.TLabel').pack(anchor='w', padx=10, pady=(20,5))
        
        self.query_results = scrolledtext.ScrolledText(self.query_frame, wrap=tk.WORD, width=100, height=25)
        self.query_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def setup_schema_frame(self):
        header_frame = ttk.Frame(self.schema_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(header_frame, text="← Back to Main Menu", 
                  command=lambda: self.show_frame(self.main_menu_frame)).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(header_frame, text="Database Schema", style='Title.TLabel').pack(side=tk.LEFT, padx=20)
        
        self.schema_text = scrolledtext.ScrolledText(self.schema_frame, wrap=tk.WORD, width=100, height=30)
        self.schema_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("SQL Error", f"Error executing SQL:\n{str(e)}")
            return False
    
    def drop_tables(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to drop all tables?"):
            tables = [
                'DentalAction_Inventory', 'Inventory', 'Bill', 'Prescription', 
                'Treatment', 'Dental_Action', 'Appointment_Staff', 'Receptionist',
                'Dental_Assistant', 'Dentist', 'Staff_Schedule', 'Staff',
                'Appointment', 'Room', 'Patient'
            ]
            
            for table in tables:
                self.execute_sql(f"DROP TABLE IF EXISTS {table}")
            
            self.menu_status.config(text="✅ All tables dropped successfully!")
            messagebox.showinfo("Success", "All tables dropped successfully!")
    
    def create_tables(self):
        # Create all tables for dental clinic system
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS Patient (
                patient_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                date_of_birth TEXT,
                street TEXT,
                city TEXT,
                province TEXT,
                postal_code TEXT,
                gender TEXT,
                phone TEXT,
                email TEXT UNIQUE,
                medical_history TEXT,
                insurance TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Room (
                room_number INTEGER PRIMARY KEY,
                room_type TEXT,
                capacity INTEGER DEFAULT 0,
                availability TEXT DEFAULT 'Y' CHECK (availability IN ('Y', 'N'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Appointment (
                appointment_id INTEGER PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                room_number INTEGER NOT NULL,
                appointment_datetime TEXT NOT NULL,
                status TEXT DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'COMPLETED', 'CANCELLED')),
                FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
                FOREIGN KEY (room_number) REFERENCES Room(room_number)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Staff (
                staff_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                salary REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Dental_Action (
                dental_action_id INTEGER PRIMARY KEY,
                appointment_id INTEGER NOT NULL,
                cost REAL,
                FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Treatment (
                treatment_id INTEGER PRIMARY KEY,
                dental_action_id INTEGER NOT NULL,
                description TEXT,
                type TEXT,
                FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Bill (
                bill_id INTEGER PRIMARY KEY,
                dental_action_id INTEGER NOT NULL,
                total_amount REAL,
                status TEXT DEFAULT 'UNPAID' CHECK (status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID')),
                issue_date TEXT,
                FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
            )
            """
        ]
        
        for sql in tables_sql:
            if not self.execute_sql(sql):
                return
        
        self.menu_status.config(text="✅ All tables created successfully!")
        messagebox.showinfo("Success", "All tables created successfully!")
    
    def populate_tables(self):
        # Insert sample data
        sample_data = [
            # Patients
            "INSERT OR IGNORE INTO Patient VALUES (1, 'John Doe', '2000-01-01', '123 Main St', 'Toronto', 'ON', 'M5V1E3', 'Male', '647-123-1234', 'john.doe@email.com', 'No allergies', 'SunLife')",
            "INSERT OR IGNORE INTO Patient VALUES (2, 'Jane Smith', '1995-05-15', '456 Oak Ave', 'Toronto', 'ON', 'M5V2B2', 'Female', '416-555-1234', 'jane.smith@email.com', 'Asthma', 'Manulife')",
            
            # Rooms
            "INSERT OR IGNORE INTO Room VALUES (100, 'Surgery', 1, 'Y')",
            "INSERT OR IGNORE INTO Room VALUES (101, 'Consultation', 1, 'Y')",
            
            # Appointments
            "INSERT OR IGNORE INTO Appointment VALUES (1000, 1, 100, '2024-01-15 09:30:00', 'COMPLETED')",
            "INSERT OR IGNORE INTO Appointment VALUES (1001, 2, 101, '2024-01-16 10:00:00', 'SCHEDULED')",
            
            # Dental Actions
            "INSERT OR IGNORE INTO Dental_Action VALUES (400, 1000, 150.00)",
            "INSERT OR IGNORE INTO Dental_Action VALUES (401, 1001, 200.00)",
            
            # Treatments
            "INSERT OR IGNORE INTO Treatment VALUES (500, 400, 'Teeth Cleaning', 'Hygiene')",
            "INSERT OR IGNORE INTO Treatment VALUES (501, 401, 'Root Canal', 'Surgery')",
            
            # Bills
            "INSERT OR IGNORE INTO Bill VALUES (800, 400, 150.00, 'PAID', '2024-01-15')",
            "INSERT OR IGNORE INTO Bill VALUES (801, 401, 200.00, 'UNPAID', '2024-01-16')"
        ]
        
        for sql in sample_data:
            if not self.execute_sql(sql):
                return
        
        self.menu_status.config(text="✅ Sample data populated successfully!")
        messagebox.showinfo("Success", "Sample data populated successfully!")
    
    def run_predefined_query(self):
        query_map = {
            "Least Popular Treatments": """
                SELECT type, COUNT(*) as num_treatments
                FROM Treatment
                GROUP BY type
                HAVING COUNT(*) <= 3
                ORDER BY num_treatments DESC
            """,
            "Patients with Both Treatments & Prescriptions": """
                SELECT p.patient_id, p.full_name
                FROM Patient p
                JOIN Appointment a ON p.patient_id = a.patient_id
                JOIN Dental_Action da ON a.appointment_id = da.appointment_id
                JOIN Treatment t ON da.dental_action_id = t.dental_action_id
            """,
            "Patients with Appointments but No Bills": """
                SELECT DISTINCT p.patient_id, p.full_name
                FROM Patient p
                JOIN Appointment a ON p.patient_id = a.patient_id
                WHERE p.patient_id NOT IN (
                    SELECT DISTINCT p2.patient_id
                    FROM Patient p2
                    JOIN Appointment a2 ON p2.patient_id = a2.patient_id
                    JOIN Dental_Action da ON a2.appointment_id = da.appointment_id
                    JOIN Bill b ON da.dental_action_id = b.dental_action_id
                )
            """,
            "Most Expensive Dental Actions": """
                SELECT p.full_name, MAX(da.cost) as highest_cost
                FROM Dental_Action da
                JOIN Appointment a ON da.appointment_id = a.appointment_id
                JOIN Patient p ON a.patient_id = p.patient_id
                GROUP BY p.full_name
                ORDER BY highest_cost DESC
            """,
            "Patient Billing Summary": """
                SELECT p.full_name, 
                       COUNT(b.bill_id) as num_bills,
                       SUM(b.total_amount) as total_billed,
                       ROUND(AVG(b.total_amount), 2) as avg_bill
                FROM Bill b
                JOIN Dental_Action da ON b.dental_action_id = da.dental_action_id
                JOIN Appointment a ON da.appointment_id = a.appointment_id
                JOIN Patient p ON a.patient_id = p.patient_id
                GROUP BY p.full_name
                ORDER BY total_billed DESC
            """
        }
        
        selected_query = self.query_var.get()
        if selected_query in query_map:
            self.execute_and_display_query(query_map[selected_query], selected_query)
        else:
            messagebox.showwarning("Warning", "Please select a query to run.")
    
    def execute_and_display_query(self, query, query_name):
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            
            self.query_results.delete(1.0, tk.END)
            self.query_results.insert(tk.END, f"Query: {query_name}\n")
            self.query_results.insert(tk.END, "=" * 80 + "\n\n")
            
            if rows:
                header = " | ".join(f"{col:<20}" for col in columns)
                self.query_results.insert(tk.END, header + "\n")
                self.query_results.insert(tk.END, "-" * len(header) + "\n")
                
                for row in rows:
                    row_str = " | ".join(f"{str(val):<20}" for val in row)
                    self.query_results.insert(tk.END, row_str + "\n")
                
                self.query_results.insert(tk.END, f"\n{len(rows)} row(s) returned\n")
            else:
                self.query_results.insert(tk.END, "No results found.\n")
                
        except Exception as e:
            self.query_results.delete(1.0, tk.END)
            self.query_results.insert(tk.END, f"Error executing query:\n{str(e)}")
    
    def show_schema(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.cursor.fetchall()
            
            schema_info = "DATABASE SCHEMA - SQLite\n"
            schema_info += "=" * 50 + "\n\n"
            
            for table in tables:
                table_name = table[0]
                schema_info += f"TABLE: {table_name}\n"
                schema_info += "-" * 40 + "\n"
                
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                columns = self.cursor.fetchall()
                
                for col in columns:
                    schema_info += f"  {col[1]:<25} {col[2]:<15} "
                    schema_info += "PRIMARY KEY" if col[5] == 1 else ""
                    schema_info += "\n"
                
                schema_info += "\n"
            
            self.schema_text.delete(1.0, tk.END)
            self.schema_text.insert(tk.END, schema_info)
            self.show_frame(self.schema_frame)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving schema:\n{str(e)}")
    
    def interactive_sql(self):
        sql_window = tk.Toplevel(self.root)
        sql_window.title("Interactive SQL Query")
        sql_window.geometry("800x600")
        
        ttk.Label(sql_window, text="Enter SQL Query:").pack(anchor='w', padx=10, pady=5)
        
        sql_text = scrolledtext.ScrolledText(sql_window, wrap=tk.WORD, width=80, height=10)
        sql_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        button_frame = ttk.Frame(sql_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(sql_window, text="Results:").pack(anchor='w', padx=10, pady=(10,5))
        
        results_text = scrolledtext.ScrolledText(sql_window, wrap=tk.WORD, width=80, height=20)
        results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def execute_sql():
            query = sql_text.get(1.0, tk.END).strip()
            if not query:
                messagebox.showwarning("Warning", "Please enter a SQL query.")
                return
            
            try:
                self.cursor.execute(query)
                
                if query.upper().startswith('SELECT'):
                    columns = [desc[0] for desc in self.cursor.description]
                    rows = self.cursor.fetchall()
                    
                    results_text.delete(1.0, tk.END)
                    
                    if rows:
                        header = " | ".join(f"{col:<20}" for col in columns)
                        results_text.insert(tk.END, header + "\n")
                        results_text.insert(tk.END, "-" * len(header) + "\n")
                        
                        for row in rows:
                            row_str = " | ".join(f"{str(val):<20}" for val in row)
                            results_text.insert(tk.END, row_str + "\n")
                        
                        results_text.insert(tk.END, f"\n{len(rows)} row(s) returned\n")
                    else:
                        results_text.insert(tk.END, "No results found.\n")
                else:
                    self.connection.commit()
                    results_text.delete(1.0, tk.END)
                    results_text.insert(tk.END, f"✅ Query executed successfully. {self.cursor.rowcount} row(s) affected.\n")
                    
            except Exception as e:
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        
        ttk.Button(button_frame, text="Execute", command=execute_sql).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: sql_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
    
    def exit_app(self):
        if self.connection:
            self.connection.close()
        self.root.quit()

def main():
    root = tk.Tk()
    app = DentalClinicApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()