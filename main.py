import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental Clinic - Database Connection")
        self.root.geometry("500x400")
        self.root.configure(bg='#f5f5f5')
        
        # Center the window
        self.center_window()
        
        self.db_file = "dental_clinic.db"
        self.connection = None
        self.cursor = None
        
        self.setup_login_ui()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_login_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = ttk.Label(main_frame, text="🦷 Dental Clinic Management", 
                               font=('Arial', 18, 'bold'), foreground='#2c3e50')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="Database Connection", 
                                  font=('Arial', 12), foreground='#7f8c8d')
        subtitle_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Username
        ttk.Label(form_frame, text="Username:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=10)
        self.username_entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, pady=10, padx=(10, 0))
        self.username_entry.insert(0, "admin")  # Default username
        
        # Password
        ttk.Label(form_frame, text="Password:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=10)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*", font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, pady=10, padx=(10, 0))
        self.password_entry.insert(0, "admin")  # Default password
        
        # Database file info
        ttk.Label(form_frame, text="Database:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=10)
        db_label = ttk.Label(form_frame, text=self.db_file, font=('Arial', 10), foreground='#27ae60')
        db_label.grid(row=2, column=1, sticky='w', pady=10, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Test Connection button
        test_btn = ttk.Button(button_frame, text="Test Connection", 
                             command=self.test_connection, width=20)
        test_btn.pack(side=tk.LEFT, padx=5)
        
        # Connect button
        connect_btn = ttk.Button(button_frame, text="Connect & Login", 
                                command=self.connect_and_login, width=20)
        connect_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=('Arial', 10))
        self.status_label.pack(pady=10)
        
        # Info text
        info_text = "Note: This is a SQLite database connection.\nDefault credentials: admin/admin"
        info_label = ttk.Label(main_frame, text=info_text, font=('Arial', 9), 
                              foreground='#7f8c8d', justify=tk.CENTER)
        info_label.pack(pady=20)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.connect_and_login())
    
    def test_connection(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="❌ Please enter username and password", foreground='#e74c3c')
            return
        
        # Simple authentication (in real app, this would be more secure)
        if username != "admin" or password != "admin":
            self.status_label.config(text="❌ Invalid credentials", foreground='#e74c3c')
            return
        
        try:
            # Test database connection
            test_conn = sqlite3.connect(self.db_file)
            test_cursor = test_conn.cursor()
            test_cursor.execute("SELECT 1")
            test_conn.close()
            
            self.status_label.config(text="✅ Connection successful! Click 'Connect & Login' to proceed.", 
                                   foreground='#27ae60')
            messagebox.showinfo("Connection Test", "✅ Database connection successful!\n\nYou can now login to the system.")
        except Exception as e:
            self.status_label.config(text=f"❌ Connection failed: {str(e)}", foreground='#e74c3c')
            messagebox.showerror("Connection Error", f"Failed to connect to database:\n{str(e)}")
    
    def connect_and_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="❌ Please enter username and password", foreground='#e74c3c')
            return
        
        # Simple authentication
        if username != "admin" or password != "admin":
            self.status_label.config(text="❌ Invalid credentials", foreground='#e74c3c')
            messagebox.showerror("Login Failed", "Invalid username or password")
            return
        
        try:
            # Connect to database
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            
            # Create tables if they don't exist
            self.create_tables()
            self.populate_tables()
            
            self.status_label.config(text="✅ Logged in successfully! Opening application...", 
                                   foreground='#27ae60')
            
            # Close login window and open main application
            self.root.after(500, self.open_main_application)
            
        except Exception as e:
            self.status_label.config(text=f"❌ Login failed: {str(e)}", foreground='#e74c3c')
            messagebox.showerror("Login Error", f"Failed to login:\n{str(e)}")
    
    def open_main_application(self):
        # Close login window
        self.root.destroy()
        
        # Open main application window
        main_root = tk.Tk()
        app = DentalClinicApp(main_root, self.connection, self.cursor)
        main_root.mainloop()
    
    def create_tables(self):
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
            CREATE TABLE IF NOT EXISTS Staff (
                staff_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                salary REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Staff_Schedule (
                schedule_id INTEGER PRIMARY KEY,
                staff_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Dentist (
                staff_id INTEGER PRIMARY KEY,
                license_no TEXT,
                specialization TEXT,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Dental_Assistant (
                staff_id INTEGER PRIMARY KEY,
                certification TEXT,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Receptionist (
                staff_id INTEGER PRIMARY KEY,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
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
            CREATE TABLE IF NOT EXISTS Appointment_Staff (
                appointment_id INTEGER NOT NULL,
                staff_id INTEGER NOT NULL,
                PRIMARY KEY (appointment_id, staff_id),
                FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id),
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
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
            CREATE TABLE IF NOT EXISTS Prescription (
                prescription_id INTEGER PRIMARY KEY,
                dental_action_id INTEGER NOT NULL,
                medication TEXT NOT NULL,
                dosage TEXT,
                duration TEXT,
                FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Inventory (
                item_id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                supplier TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS DentalAction_Inventory (
                dental_action_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity_used INTEGER NOT NULL,
                PRIMARY KEY (dental_action_id, item_id),
                FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id),
                FOREIGN KEY (item_id) REFERENCES Inventory(item_id)
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
            self.cursor.execute(sql)
        
        self.connection.commit()
    
    def populate_tables(self):
        # Check if data already exists
        self.cursor.execute("SELECT COUNT(*) FROM Patient")
        if self.cursor.fetchone()[0] > 0:
            return  # Data already populated
        
        sample_data = [
            # Patients
            "INSERT INTO Patient VALUES (1, 'John Doe', '2000-01-01', '123 Main St', 'Toronto', 'ON', 'M5V1E3', 'Male', '647-123-1234', 'john.doe@email.com', 'No allergies', 'SunLife')",
            "INSERT INTO Patient VALUES (2, 'Jane Smith', '1995-05-15', '456 Oak Ave', 'Toronto', 'ON', 'M5V2B2', 'Female', '416-555-1234', 'jane.smith@email.com', 'Asthma', 'Manulife')",
            "INSERT INTO Patient VALUES (3, 'Bob Johnson', '1988-11-20', '789 Pine Rd', 'Mississauga', 'ON', 'L5A3K2', 'Male', '905-444-5678', 'bob.johnson@email.com', 'Diabetes', 'BlueCross')",
            "INSERT INTO Patient VALUES (4, 'Alice Williams', '1992-03-10', '321 Elm St', 'Toronto', 'ON', 'M4C2N1', 'Female', '647-777-8888', 'alice.w@email.com', 'None', 'SunLife')",
            
            # Rooms
            "INSERT INTO Room VALUES (100, 'Surgery', 1, 'Y')",
            "INSERT INTO Room VALUES (101, 'Consultation', 1, 'Y')",
            "INSERT INTO Room VALUES (102, 'X-Ray', 1, 'N')",
            "INSERT INTO Room VALUES (103, 'Cleaning', 1, 'Y')",
            
            # Staff
            "INSERT INTO Staff VALUES (1, 'Dr. Sarah Johnson', '416-111-2222', 'sjohnson@dental.com', 120000.00)",
            "INSERT INTO Staff VALUES (2, 'Dr. Michael Chen', '416-222-3333', 'mchen@dental.com', 125000.00)",
            "INSERT INTO Staff VALUES (3, 'Emily Brown', '416-333-4444', 'ebrown@dental.com', 45000.00)",
            "INSERT INTO Staff VALUES (4, 'David Lee', '416-444-5555', 'dlee@dental.com', 42000.00)",
            "INSERT INTO Staff VALUES (5, 'Jessica Martinez', '416-555-6666', 'jmartinez@dental.com', 38000.00)",
            
            # Dentists
            "INSERT INTO Dentist VALUES (1, 'DEN-2018-0123', 'Orthodontics')",
            "INSERT INTO Dentist VALUES (2, 'DEN-2019-0456', 'Endodontics')",
            
            # Dental Assistants
            "INSERT INTO Dental_Assistant VALUES (3, 'Certified Dental Assistant Level II')",
            "INSERT INTO Dental_Assistant VALUES (4, 'Certified Dental Assistant Level I')",
            
            # Receptionists
            "INSERT INTO Receptionist VALUES (5)",
            
            # Staff Schedules
            "INSERT INTO Staff_Schedule VALUES (1, 1, '2024-01-15 08:00:00', '2024-01-15 16:00:00')",
            "INSERT INTO Staff_Schedule VALUES (2, 2, '2024-01-15 09:00:00', '2024-01-15 17:00:00')",
            "INSERT INTO Staff_Schedule VALUES (3, 3, '2024-01-15 08:00:00', '2024-01-15 16:00:00')",
            "INSERT INTO Staff_Schedule VALUES (4, 4, '2024-01-16 08:00:00', '2024-01-16 16:00:00')",
            "INSERT INTO Staff_Schedule VALUES (5, 5, '2024-01-15 07:30:00', '2024-01-15 15:30:00')",
            
            # Appointments
            "INSERT INTO Appointment VALUES (1000, 1, 100, '2024-01-15 09:30:00', 'COMPLETED')",
            "INSERT INTO Appointment VALUES (1001, 2, 101, '2024-01-16 10:00:00', 'SCHEDULED')",
            "INSERT INTO Appointment VALUES (1002, 3, 100, '2024-01-17 14:00:00', 'COMPLETED')",
            "INSERT INTO Appointment VALUES (1003, 4, 103, '2024-01-18 11:00:00', 'COMPLETED')",
            "INSERT INTO Appointment VALUES (1004, 1, 101, '2024-01-19 15:00:00', 'SCHEDULED')",
            
            # Appointment_Staff
            "INSERT INTO Appointment_Staff VALUES (1000, 1)",
            "INSERT INTO Appointment_Staff VALUES (1000, 3)",
            "INSERT INTO Appointment_Staff VALUES (1001, 2)",
            "INSERT INTO Appointment_Staff VALUES (1001, 4)",
            "INSERT INTO Appointment_Staff VALUES (1002, 1)",
            "INSERT INTO Appointment_Staff VALUES (1002, 3)",
            "INSERT INTO Appointment_Staff VALUES (1003, 2)",
            
            # Dental Actions
            "INSERT INTO Dental_Action VALUES (400, 1000, 150.00)",
            "INSERT INTO Dental_Action VALUES (401, 1001, 200.00)",
            "INSERT INTO Dental_Action VALUES (402, 1002, 500.00)",
            "INSERT INTO Dental_Action VALUES (403, 1003, 75.00)",
            "INSERT INTO Dental_Action VALUES (404, 1000, 100.00)",
            
            # Treatments
            "INSERT INTO Treatment VALUES (500, 400, 'Teeth Cleaning', 'Hygiene')",
            "INSERT INTO Treatment VALUES (501, 401, 'Root Canal', 'Surgery')",
            "INSERT INTO Treatment VALUES (502, 402, 'Tooth Extraction', 'Surgery')",
            "INSERT INTO Treatment VALUES (503, 403, 'Dental Checkup', 'Examination')",
            "INSERT INTO Treatment VALUES (504, 404, 'Fluoride Treatment', 'Hygiene')",
            
            # Prescriptions
            "INSERT INTO Prescription VALUES (1, 401, 'Amoxicillin', '500mg', '7 days')",
            "INSERT INTO Prescription VALUES (2, 402, 'Ibuprofen', '400mg', '5 days')",
            "INSERT INTO Prescription VALUES (3, 401, 'Hydrocodone', '5mg', '3 days')",
            
            # Inventory
            "INSERT INTO Inventory VALUES (1, 'Dental Gloves', 500, 'MedSupply Inc')",
            "INSERT INTO Inventory VALUES (2, 'Anesthetic Cartridges', 200, 'DentalPro')",
            "INSERT INTO Inventory VALUES (3, 'Dental Floss', 300, 'OralCare Co')",
            "INSERT INTO Inventory VALUES (4, 'Surgical Masks', 1000, 'SafetyFirst')",
            "INSERT INTO Inventory VALUES (5, 'Fluoride Gel', 50, 'DentalPro')",
            
            # DentalAction_Inventory
            "INSERT INTO DentalAction_Inventory VALUES (400, 1, 2)",
            "INSERT INTO DentalAction_Inventory VALUES (400, 3, 1)",
            "INSERT INTO DentalAction_Inventory VALUES (401, 1, 2)",
            "INSERT INTO DentalAction_Inventory VALUES (401, 2, 3)",
            "INSERT INTO DentalAction_Inventory VALUES (402, 1, 2)",
            "INSERT INTO DentalAction_Inventory VALUES (402, 2, 5)",
            "INSERT INTO DentalAction_Inventory VALUES (404, 5, 1)",
            
            # Bills
            "INSERT INTO Bill VALUES (800, 400, 150.00, 'PAID', '2024-01-15')",
            "INSERT INTO Bill VALUES (801, 401, 200.00, 'UNPAID', '2024-01-16')",
            "INSERT INTO Bill VALUES (802, 402, 500.00, 'PARTIALLY_PAID', '2024-01-17')",
            "INSERT INTO Bill VALUES (803, 403, 75.00, 'PAID', '2024-01-18')"
        ]
        
        try:
            for sql in sample_data:
                self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error populating tables: {str(e)}")
            raise


class DentalClinicApp:
    def __init__(self, root, connection, cursor):
        self.root = root
        self.root.title("Dental Clinic Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Use passed connection and cursor
        self.connection = connection
        self.cursor = cursor
        self.db_file = "dental_clinic.db"
        
        # Track current table and selected row
        self.current_table = None
        self.selected_row = None
        
        # Setup UI
        self.setup_ui()
        
        # Update dashboard stats
        self.root.after(100, self.update_dashboard_stats)
        self.root.after(100, self.populate_table_list)
    
    def setup_ui(self):
        self.setup_styles()
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for each tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.query_frame = ttk.Frame(self.notebook)
        self.tables_frame = ttk.Frame(self.notebook)
        self.schema_frame = ttk.Frame(self.notebook)
        self.sql_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.dashboard_frame, text="🏠 Dashboard")
        self.notebook.add(self.query_frame, text="🔍 Query Builder")
        self.notebook.add(self.tables_frame, text="📊 Browse Tables")
        self.notebook.add(self.schema_frame, text="📋 Schema")
        self.notebook.add(self.sql_frame, text="⚡ SQL Console")
        self.notebook.add(self.search_frame, text="🔎 Search Records")
        
        self.setup_dashboard()
        self.setup_query_frame()
        self.setup_tables_frame()
        self.setup_schema_frame()
        self.setup_sql_frame()
        self.setup_search_frame()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 12), foreground='#7f8c8d')
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        style.configure('Card.TLabel', background='white', font=('Arial', 10))
        style.configure('Success.TLabel', foreground='#27ae60', font=('Arial', 9))
        style.configure('Warning.TLabel', foreground='#e67e22', font=('Arial', 9))
        style.configure('Custom.TButton', font=('Arial', 10), padding=(10, 5))
        style.configure('Danger.TButton', font=('Arial', 10), padding=(10, 5), background='#e74c3c')
    
    def setup_dashboard(self):
        # Header
        header_frame = ttk.Frame(self.dashboard_frame)
        header_frame.pack(fill=tk.X, pady=20)
        
        title_label = ttk.Label(header_frame, text="Dental Clinic Management System", style='Title.TLabel')
        title_label.pack()
        
        subtitle = ttk.Label(header_frame, text="Professional Database Management Interface", style='Subtitle.TLabel')
        subtitle.pack(pady=5)
        
        # Connection status
        self.connection_status = ttk.Label(header_frame, text="✅ Connected to database", style='Success.TLabel')
        self.connection_status.pack()
        
        # Stats cards
        stats_frame = ttk.Frame(self.dashboard_frame)
        stats_frame.pack(fill=tk.X, pady=20)
        
        stats_data = [
            ("Patients", "SELECT COUNT(*) FROM Patient", "👥"),
            ("Staff", "SELECT COUNT(*) FROM Staff", "👨‍⚕️"),
            ("Appointments", "SELECT COUNT(*) FROM Appointment", "📅"),
            ("Treatments", "SELECT COUNT(*) FROM Treatment", "🦷"),
            ("Prescriptions", "SELECT COUNT(*) FROM Prescription", "💊"),
            ("Inventory Items", "SELECT COUNT(*) FROM Inventory", "📦"),
            ("Bills", "SELECT COUNT(*) FROM Bill", "💰"),
            ("Dentists", "SELECT COUNT(*) FROM Dentist", "🩺")
        ]
        
        for i, (title, query, icon) in enumerate(stats_data):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.grid(row=i//4, column=i%4, padx=10, pady=10, sticky='nsew')
            stats_frame.columnconfigure(i%4, weight=1)
            
            # Card content
            ttk.Label(card, text=icon, style='Card.TLabel', font=('Arial', 20)).pack(pady=5)
            ttk.Label(card, text=title, style='Card.TLabel', font=('Arial', 11, 'bold')).pack()
            count_label = ttk.Label(card, text="Loading...", style='Card.TLabel', font=('Arial', 14, 'bold'))
            count_label.pack(pady=5)
            
            # Store reference to update later
            setattr(self, f"{title.lower().replace(' ', '_')}_count", count_label)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(self.dashboard_frame, text="Quick Actions", padding=15)
        actions_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        actions = [
            ("🗑️ Reset Database", "Drop and recreate all tables with sample data", self.reset_database),
            ("🔄 Test Connection", "Verify database connectivity", self.test_connection),
            ("📊 View All Tables", "Browse all database tables", lambda: self.notebook.select(2)),
            ("🔍 Run Queries", "Execute analytical queries", lambda: self.notebook.select(1)),
            ("📋 View Schema", "Database structure overview", lambda: self.notebook.select(3)),
            ("⚡ SQL Console", "Execute custom SQL commands", lambda: self.notebook.select(4)),
            ("🔎 Search Records", "Search for specific records", lambda: self.notebook.select(5))
        ]
        
        for i, (text, description, command) in enumerate(actions):
            btn_frame = ttk.Frame(actions_frame)
            btn_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            actions_frame.columnconfigure(i%3, weight=1)
            actions_frame.rowconfigure(i//3, weight=1)
            
            btn = ttk.Button(btn_frame, text=text, command=command, style='Custom.TButton')
            btn.pack(fill=tk.X)
            
            desc_label = ttk.Label(btn_frame, text=description, font=('Arial', 8), foreground='#666', 
                                 wraplength=200, justify=tk.CENTER)
            desc_label.pack(fill=tk.X, pady=(2, 0))
    
    def setup_query_frame(self):
        # Query selection section
        query_selection_frame = ttk.LabelFrame(self.query_frame, text="Query Builder", padding=15)
        query_selection_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Query dropdown with descriptions
        self.query_var = tk.StringVar()
        self.queries = [
            ("Find least popular treatment types (occur less than 3 times)", "least_popular_treatments"),
            ("Find patients who had both treatments and prescriptions", "patients_both_treatment_prescription"),
            ("Find patients with appointments but no bills generated", "patients_no_bills"),
            ("Find the most expensive dental actions per patient", "most_expensive_actions"),
            ("Find patients who had appointments but no treatments", "patients_no_treatments"),
            ("Show inventory items used in treatments involving dentists", "inventory_used_by_dentists"),
            ("Patient billing summary (total billed, average bill amount)", "patient_billing_summary"),
            ("List all staff members and their roles", "staff_with_roles"),
            ("Show appointments with assigned staff", "appointments_with_staff"),
            ("Inventory usage report", "inventory_usage_report")
        ]
        
        ttk.Label(query_selection_frame, text="Choose a query:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        query_combo = ttk.Combobox(query_selection_frame, textvariable=self.query_var, 
                                  values=[q[0] for q in self.queries], state="readonly", 
                                  width=80, font=('Arial', 10))
        query_combo.pack(fill=tk.X, pady=5)
        query_combo.set("Select a query from the dropdown...")
        
        # Execute button
        execute_frame = ttk.Frame(query_selection_frame)
        execute_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(execute_frame, text="Execute Query", command=self.execute_selected_query, 
                  style='Custom.TButton').pack(side=tk.LEFT)
        
        self.query_status = ttk.Label(execute_frame, text="", style='Success.TLabel')
        self.query_status.pack(side=tk.LEFT, padx=10)
        
        # Results section
        results_frame = ttk.LabelFrame(self.query_frame, text="Query Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Results info bar
        self.results_info = ttk.Label(results_frame, text="No query executed yet", 
                                     font=('Arial', 9), foreground='#666')
        self.results_info.pack(anchor='w', pady=5)
        
        # Create a frame to hold treeview and scrollbars
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for table display
        self.results_tree = ttk.Treeview(tree_frame, show='headings')
        
        # Scrollbars for treeview
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for proper scrollbar positioning
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def setup_tables_frame(self):
        # Table selection
        selection_frame = ttk.LabelFrame(self.tables_frame, text="Table Browser", padding=15)
        selection_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(selection_frame, text="Choose a table to view:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        table_selection_frame = ttk.Frame(selection_frame)
        table_selection_frame.pack(fill=tk.X, pady=5)
        
        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(table_selection_frame, textvariable=self.table_var, 
                                       state="readonly", width=40, font=('Arial', 10))
        self.table_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(table_selection_frame, text="Load Table", command=self.load_table_data, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(table_selection_frame, text="Refresh", command=self.populate_table_list, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        # Table actions frame
        actions_frame = ttk.Frame(selection_frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="➕ Add New Record", command=self.add_record, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="✏️ Edit Selected", command=self.edit_record, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="🗑️ Delete Selected", command=self.delete_record, 
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        self.table_action_status = ttk.Label(actions_frame, text="", style='Success.TLabel')
        self.table_action_status.pack(side=tk.LEFT, padx=10)
        
        # Table display
        table_display_frame = ttk.LabelFrame(self.tables_frame, text="Table Data", padding=10)
        table_display_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Results info
        self.table_info = ttk.Label(table_display_frame, text="Select a table to view data", 
                                   font=('Arial', 9), foreground='#666')
        self.table_info.pack(anchor='w', pady=5)
        
        # Create a frame to hold treeview and scrollbars
        tree_frame = ttk.Frame(table_display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for table data
        self.table_tree = ttk.Treeview(tree_frame, show='headings')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.table_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.table_tree.xview)
        
        self.table_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for proper scrollbar positioning
        self.table_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click to edit
        self.table_tree.bind('<Double-1>', lambda e: self.edit_record())
        
        # Bind selection
        self.table_tree.bind('<<TreeviewSelect>>', self.on_table_select)
    
    def on_table_select(self, event):
        selection = self.table_tree.selection()
        if selection:
            self.selected_row = self.table_tree.item(selection[0])['values']
        else:
            self.selected_row = None
    
    def setup_schema_frame(self):
        # Header with refresh button
        header_frame = ttk.Frame(self.schema_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Database Schema", font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Refresh Schema", command=self.refresh_schema, 
                  style='Custom.TButton').pack(side=tk.RIGHT)
        
        # Schema text widget
        self.schema_text = scrolledtext.ScrolledText(self.schema_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10), width=100, height=30)
        self.schema_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load schema information
        self.refresh_schema()
    
    def refresh_schema(self):
        self.schema_text.config(state=tk.NORMAL)
        self.schema_text.delete(1.0, tk.END)
        schema_info = self.get_schema_info()
        self.schema_text.insert(tk.END, schema_info)
        self.schema_text.config(state=tk.DISABLED)
    
    def setup_sql_frame(self):
        # SQL input section
        input_frame = ttk.LabelFrame(self.sql_frame, text="SQL Console", padding=15)
        input_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(input_frame, text="Enter SQL Query:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        self.sql_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                                 font=('Consolas', 10), height=8)
        self.sql_text.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Execute", command=self.execute_custom_sql, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=lambda: self.sql_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.sql_status = ttk.Label(button_frame, text="", style='Success.TLabel')
        self.sql_status.pack(side=tk.LEFT, padx=10)
        
        # Results section
        results_frame = ttk.LabelFrame(self.sql_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.sql_results = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=('Consolas', 10))
        self.sql_results.pack(fill=tk.BOTH, expand=True)
    
    def setup_search_frame(self):
        # Search configuration section
        search_config_frame = ttk.LabelFrame(self.search_frame, text="Search Configuration", padding=15)
        search_config_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Table selection
        ttk.Label(search_config_frame, text="Search in Table:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        table_frame = ttk.Frame(search_config_frame)
        table_frame.pack(fill=tk.X, pady=5)
        
        self.search_table_var = tk.StringVar()
        self.search_table_combo = ttk.Combobox(table_frame, textvariable=self.search_table_var, 
                                              state="readonly", width=40, font=('Arial', 10))
        self.search_table_combo.pack(side=tk.LEFT, padx=5)
        
        # Column selection
        ttk.Label(search_config_frame, text="Search in Column:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        column_frame = ttk.Frame(search_config_frame)
        column_frame.pack(fill=tk.X, pady=5)
        
        self.search_column_var = tk.StringVar()
        self.search_column_combo = ttk.Combobox(column_frame, textvariable=self.search_column_var, 
                                               state="readonly", width=40, font=('Arial', 10))
        self.search_column_combo.pack(side=tk.LEFT, padx=5)
        
        # Search term
        ttk.Label(search_config_frame, text="Search Term:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        search_term_frame = ttk.Frame(search_config_frame)
        search_term_frame.pack(fill=tk.X, pady=5)
        
        self.search_term_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_term_frame, textvariable=self.search_term_var, 
                                     width=50, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search type
        self.search_type_var = tk.StringVar(value="contains")
        search_type_frame = ttk.Frame(search_term_frame)
        search_type_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(search_type_frame, text="Contains", variable=self.search_type_var, 
                       value="contains").pack(side=tk.LEFT)
        ttk.Radiobutton(search_type_frame, text="Starts With", variable=self.search_type_var, 
                       value="startswith").pack(side=tk.LEFT)
        ttk.Radiobutton(search_type_frame, text="Exact Match", variable=self.search_type_var, 
                       value="exact").pack(side=tk.LEFT)
        
        # Search button
        button_frame = ttk.Frame(search_config_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Search", command=self.execute_search, 
                  style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Results", 
                  command=self.clear_search_results).pack(side=tk.LEFT, padx=5)
        
        self.search_status = ttk.Label(button_frame, text="", style='Success.TLabel')
        self.search_status.pack(side=tk.LEFT, padx=10)
        
        # Quick search examples
        examples_frame = ttk.Frame(search_config_frame)
        examples_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(examples_frame, text="Quick Searches:", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        examples_buttons_frame = ttk.Frame(examples_frame)
        examples_buttons_frame.pack(fill=tk.X, pady=5)
        
        examples = [
            ("Find John", "Patient", "full_name", "John"),
            ("Toronto Patients", "Patient", "city", "Toronto"),
            ("Scheduled Appointments", "Appointment", "status", "SCHEDULED"),
            ("High Cost Treatments", "Dental_Action", "cost", "200"),
            ("Unpaid Bills", "Bill", "status", "UNPAID")
        ]
        
        for text, table, column, term in examples:
            btn = ttk.Button(examples_buttons_frame, text=text, 
                           command=lambda t=table, c=column, term=term: self.setup_quick_search(t, c, term),
                           width=15)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Results section
        results_frame = ttk.LabelFrame(self.search_frame, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Results info
        self.search_results_info = ttk.Label(results_frame, text="No search performed yet", 
                                           font=('Arial', 9), foreground='#666')
        self.search_results_info.pack(anchor='w', pady=5)
        
        # Create a frame to hold treeview and scrollbars
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for search results
        self.search_tree = ttk.Treeview(tree_frame, show='headings')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.search_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.search_tree.xview)
        
        self.search_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for proper scrollbar positioning
        self.search_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind table selection to update columns
        self.search_table_combo.bind('<<ComboboxSelected>>', self.update_search_columns)
        
        # Populate tables for search
        self.populate_search_tables()
    
    def populate_search_tables(self):
        if not self.cursor:
            return
        
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [table[0] for table in self.cursor.fetchall()]
            self.search_table_combo['values'] = tables
            self.table_combo['values'] = tables  # Also update the table browser combo
            
            if tables:
                self.search_table_combo.set(tables[0])
                self.update_search_columns()
        except Exception as e:
            print(f"Error loading tables: {str(e)}")
            messagebox.showerror("Error", f"Failed to load tables: {str(e)}")
    
    def update_search_columns(self, event=None):
        table_name = self.search_table_var.get()
        if not table_name:
            return
        
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in self.cursor.fetchall()]
            self.search_column_combo['values'] = columns
            if columns:
                self.search_column_combo.set(columns[0])
        except Exception as e:
            print(f"Error loading columns: {str(e)}")
    
    def setup_quick_search(self, table, column, term):
        self.search_table_var.set(table)
        self.update_search_columns()
        self.search_column_var.set(column)
        self.search_term_var.set(term)
        self.execute_search()
    
    def execute_search(self):
        table_name = self.search_table_var.get()
        column_name = self.search_column_var.get()
        search_term = self.search_term_var.get()
        search_type = self.search_type_var.get()
        
        if not table_name or not column_name or not search_term:
            messagebox.showwarning("Warning", "Please select a table, column, and enter a search term.")
            return
        
        try:
            # Clear previous results
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
            self.search_tree["columns"] = []
            
            # Build search query based on search type
            if search_type == "contains":
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
                params = (f'%{search_term}%',)
            elif search_type == "startswith":
                query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
                params = (f'{search_term}%',)
            else:  # exact match
                query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
                params = (search_term,)
            
            # Execute search
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Configure treeview
            self.search_tree["columns"] = columns
            for col in columns:
                self.search_tree.heading(col, text=col)
                self.search_tree.column(col, width=120, minwidth=50)
            
            # Insert data
            for row in rows:
                self.search_tree.insert("", tk.END, values=row)
            
            # Update status
            self.search_status.config(text=f"✅ Found {len(rows)} records")
            self.search_results_info.config(text=f"Found {len(rows)} records in {table_name} where {column_name} {search_type} '{search_term}'")
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to execute search:\n{str(e)}")
            self.search_status.config(text="❌ Search failed")
    
    def clear_search_results(self):
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        self.search_tree["columns"] = []
        self.search_results_info.config(text="No search performed yet")
        self.search_status.config(text="")
    
    # NEW METHODS FOR TABLE MODIFICATION
    def add_record(self):
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first.")
            return
        
        # Get column information
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        
        # Create edit dialog
        self.create_edit_dialog(table_name, columns, None, "Add New Record")
    
    def edit_record(self):
        if not self.selected_row:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return
        
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first.")
            return
        
        # Get column information
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        
        # Create edit dialog
        self.create_edit_dialog(table_name, columns, self.selected_row, "Edit Record")
    
    def create_edit_dialog(self, table_name, columns, row_data, title):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x600")
        dialog.configure(bg='#f5f5f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'500x600+{x}+{y}')
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"{title} - {table_name}", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Create form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        entry_widgets = {}
        
        # Create form fields
        for i, col in enumerate(columns):
            col_name, col_type, not_null, default_val, pk = col[1], col[2], col[3], col[4], col[5]
            
            # Create label
            label_text = f"{col_name} ({col_type})"
            if pk:
                label_text += " 🔑"
            if not_null:
                label_text += " *"
                
            ttk.Label(form_frame, text=label_text, font=('Arial', 10)).grid(
                row=i, column=0, sticky='w', pady=5, padx=5)
            
            # Create entry widget
            if col_type.upper() in ('TEXT', 'VARCHAR', 'CHAR'):
                entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
            elif col_type.upper() in ('INTEGER', 'INT'):
                entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
                # Add validation for integers
                entry.configure(validate='key', validatecommand=(dialog.register(self.validate_int), '%P'))
            elif col_type.upper() in ('REAL', 'FLOAT', 'DECIMAL'):
                entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
                # Add validation for floats
                entry.configure(validate='key', validatecommand=(dialog.register(self.validate_float), '%P'))
            else:
                entry = ttk.Entry(form_frame, width=40, font=('Arial', 10))
            
            # Set default value if editing existing record
            if row_data and i < len(row_data):
                entry.insert(0, str(row_data[i]))
            
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            entry_widgets[col_name] = entry
        
        form_frame.columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        if title == "Add New Record":
            ttk.Button(button_frame, text="Add Record", 
                      command=lambda: self.save_record(dialog, table_name, entry_widgets, columns, False),
                      style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        else:
            ttk.Button(button_frame, text="Update Record", 
                      command=lambda: self.save_record(dialog, table_name, entry_widgets, columns, True),
                      style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def validate_int(self, value):
        if value == "" or value.isdigit():
            return True
        return False
    
    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def save_record(self, dialog, table_name, entry_widgets, columns, is_edit):
        try:
            # Build column names and values
            col_names = []
            values = []
            primary_key_col = None
            primary_key_value = None
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = col[5]
                
                value = entry_widgets[col_name].get()
                
                # Handle empty values
                if value == "":
                    if is_pk and not is_edit:  # PK can be empty for new records (auto-increment)
                        continue
                    value = None
                else:
                    # Convert based on type
                    if col_type.upper() in ('INTEGER', 'INT'):
                        value = int(value)
                    elif col_type.upper() in ('REAL', 'FLOAT', 'DECIMAL'):
                        value = float(value)
                
                if is_pk:
                    primary_key_col = col_name
                    primary_key_value = value
                
                col_names.append(col_name)
                values.append(value)
            
            if is_edit:
                # Update existing record
                if not primary_key_col or primary_key_value is None:
                    messagebox.showerror("Error", "Cannot update record without primary key.")
                    return
                
                set_clause = ", ".join([f"{col} = ?" for col in col_names])
                query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_col} = ?"
                
                # Add primary key value at the end for WHERE clause
                values.append(primary_key_value)
            else:
                # Insert new record
                placeholders = ", ".join(["?" for _ in col_names])
                col_list = ", ".join(col_names)
                query = f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})"
            
            # Execute query
            self.cursor.execute(query, values)
            self.connection.commit()
            
            # Refresh table data
            self.load_table_data()
            self.update_dashboard_stats()
            
            dialog.destroy()
            self.table_action_status.config(text="✅ Record saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record:\n{str(e)}")
    
    def delete_record(self):
        if not self.selected_row:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first.")
            return
        
        # Get primary key column
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = self.cursor.fetchall()
        primary_key_col = None
        
        for col in columns:
            if col[5]:  # pk field
                primary_key_col = col[1]
                break
        
        if not primary_key_col:
            messagebox.showerror("Error", "Cannot delete record - no primary key found.")
            return
        
        # Find primary key value
        pk_index = None
        for i, col in enumerate(columns):
            if col[1] == primary_key_col:
                pk_index = i
                break
        
        if pk_index is None or pk_index >= len(self.selected_row):
            messagebox.showerror("Error", "Cannot delete record - primary key value not found.")
            return
        
        pk_value = self.selected_row[pk_index]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                  f"Are you sure you want to delete this record?\n\n{primary_key_col}: {pk_value}"):
            return
        
        try:
            # Delete record
            query = f"DELETE FROM {table_name} WHERE {primary_key_col} = ?"
            self.cursor.execute(query, (pk_value,))
            self.connection.commit()
            
            # Refresh table data
            self.load_table_data()
            self.update_dashboard_stats()
            
            self.table_action_status.config(text="✅ Record deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record:\n{str(e)}")
    
    def update_dashboard_stats(self):
        if not self.cursor:
            return
            
        stats_queries = {
            'patients': "SELECT COUNT(*) FROM Patient",
            'staff': "SELECT COUNT(*) FROM Staff",
            'appointments': "SELECT COUNT(*) FROM Appointment",
            'treatments': "SELECT COUNT(*) FROM Treatment",
            'prescriptions': "SELECT COUNT(*) FROM Prescription",
            'inventory_items': "SELECT COUNT(*) FROM Inventory",
            'bills': "SELECT COUNT(*) FROM Bill",
            'dentists': "SELECT COUNT(*) FROM Dentist"
        }
        
        for stat, query in stats_queries.items():
            try:
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                getattr(self, f"{stat}_count").config(text=str(count))
            except Exception as e:
                print(f"Error updating {stat}: {e}")
                getattr(self, f"{stat}_count").config(text="0")
    
    def populate_table_list(self):
        if not self.cursor:
            return
        
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [table[0] for table in self.cursor.fetchall()]
            self.table_combo['values'] = tables
            if tables:
                self.table_var.set(tables[0])
        except Exception as e:
            print(f"Error loading tables: {str(e)}")
            messagebox.showerror("Error", f"Failed to load tables: {str(e)}")
    
    def load_table_data(self):
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first.")
            return
        
        self.current_table = table_name
        
        try:
            # Clear existing treeview
            for item in self.table_tree.get_children():
                self.table_tree.delete(item)
            self.table_tree["columns"] = []
            
            # Get table data
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
            rows = self.cursor.fetchall()
            
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Configure treeview columns
            self.table_tree["columns"] = columns
            for col in columns:
                self.table_tree.heading(col, text=col)
                self.table_tree.column(col, width=120, minwidth=50)
            
            # Insert data
            for row in rows:
                self.table_tree.insert("", tk.END, values=row)
            
            # Update info label
            total_count = self.get_table_count(table_name)
            display_count = min(len(rows), 100)
            self.table_info.config(text=f"Showing 1 to {display_count} of {total_count} entries from {table_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table data: {str(e)}")
    
    def execute_selected_query(self):
        query_text = self.query_var.get()
        if not query_text or query_text == "Select a query from the dropdown...":
            messagebox.showwarning("Warning", "Please select a query from the dropdown.")
            return
        
        # Find the corresponding query SQL
        query_sql = None
        for desc, key in self.queries:
            if desc == query_text:
                query_sql = self.get_query_sql(key)
                break
        
        if not query_sql:
            messagebox.showerror("Error", "Selected query not found.")
            return
        
        try:
            # Clear previous results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            self.results_tree["columns"] = []
            
            # Execute query
            self.cursor.execute(query_sql)
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            
            # Configure treeview
            self.results_tree["columns"] = columns
            for col in columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, width=120, minwidth=50)
            
            # Insert data
            for row in rows:
                self.results_tree.insert("", tk.END, values=row)
            
            # Update status
            self.query_status.config(text=f"✅ Query executed successfully")
            self.results_info.config(text=f"Showing 1 to {len(rows)} of {len(rows)} entries")
            
        except Exception as e:
            messagebox.showerror("Query Error", f"Failed to execute query:\n{str(e)}")
            self.query_status.config(text="❌ Query failed")
    
    def execute_custom_sql(self):
        query = self.sql_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query.")
            return
        
        try:
            self.cursor.execute(query)
            
            if query.upper().startswith('SELECT'):
                columns = [desc[0] for desc in self.cursor.description]
                rows = self.cursor.fetchall()
                
                self.sql_results.delete(1.0, tk.END)
                
                if rows:
                    # Format as table
                    header = " | ".join(f"{col:<20}" for col in columns)
                    self.sql_results.insert(tk.END, header + "\n")
                    self.sql_results.insert(tk.END, "-" * len(header) + "\n")
                    
                    for row in rows:
                        row_str = " | ".join(f"{str(val):<20}" for val in row)
                        self.sql_results.insert(tk.END, row_str + "\n")
                    
                    self.sql_results.insert(tk.END, f"\n{len(rows)} row(s) returned\n")
                else:
                    self.sql_results.insert(tk.END, "No results found.\n")
            else:
                self.connection.commit()
                self.sql_results.delete(1.0, tk.END)
                self.sql_results.insert(tk.END, f"✅ Query executed successfully. {self.cursor.rowcount} row(s) affected.\n")
            
            self.sql_status.config(text="✅ Query executed")
            self.update_dashboard_stats()  # Refresh stats after potential changes
            
        except Exception as e:
            self.sql_results.delete(1.0, tk.END)
            self.sql_results.insert(tk.END, f"❌ Error: {str(e)}\n")
            self.sql_status.config(text="❌ Query failed")
    
    def get_query_sql(self, query_key):
        queries = {
            "least_popular_treatments": """
                SELECT t.type, COUNT(*) AS num_treatments
                FROM Treatment t
                GROUP BY t.type
                HAVING COUNT(*) <= 3
                ORDER BY num_treatments DESC
            """,
            "patients_both_treatment_prescription": """
                SELECT p.patient_id, p.full_name
                FROM Patient p
                JOIN Appointment a ON a.patient_id = p.patient_id
                JOIN Dental_Action da ON a.appointment_id = da.appointment_id
                JOIN Treatment t ON t.dental_action_id = da.dental_action_id
                INTERSECT
                SELECT p.patient_id, p.full_name
                FROM Patient p
                JOIN Appointment a ON a.patient_id = p.patient_id
                JOIN Dental_Action da ON a.appointment_id = da.appointment_id
                JOIN Prescription pr ON pr.dental_action_id = da.dental_action_id
            """,
            "patients_no_bills": """
                SELECT DISTINCT p.patient_id, p.full_name
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Bill b
                    JOIN Dental_Action da ON b.dental_action_id = da.dental_action_id
                    WHERE da.appointment_id = a.appointment_id
                )
            """,
            "most_expensive_actions": """
                SELECT p.full_name, MAX(da.cost) AS highest_cost
                FROM Dental_Action da
                JOIN Appointment a ON da.appointment_id = a.appointment_id
                JOIN Patient p ON a.patient_id = p.patient_id
                GROUP BY p.full_name
                ORDER BY highest_cost DESC
            """,
            "patients_no_treatments": """
                SELECT p.patient_id, p.full_name
                FROM Patient p
                JOIN Appointment a ON p.patient_id = a.patient_id
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Dental_Action da
                    JOIN Treatment t ON da.dental_action_id = t.dental_action_id
                    WHERE da.appointment_id = a.appointment_id
                )
            """,
            "inventory_used_by_dentists": """
                SELECT DISTINCT i.item_name, i.supplier, s.name AS dentist_name
                FROM Inventory i
                JOIN DentalAction_Inventory dai ON i.item_id = dai.item_id
                JOIN Dental_Action da ON dai.dental_action_id = da.dental_action_id
                JOIN Appointment a ON da.appointment_id = a.appointment_id
                JOIN Appointment_Staff ast ON a.appointment_id = ast.appointment_id
                JOIN Dentist d ON ast.staff_id = d.staff_id
                JOIN Staff s ON d.staff_id = s.staff_id
                ORDER BY dentist_name, item_name
            """,
            "patient_billing_summary": """
                SELECT p.full_name, 
                       COUNT(b.bill_id) AS num_bills,
                       SUM(b.total_amount) AS total_billed, 
                       ROUND(AVG(b.total_amount),2) AS avg_bill
                FROM Bill b
                JOIN Dental_Action da ON b.dental_action_id = da.dental_action_id
                JOIN Appointment a ON da.appointment_id = a.appointment_id
                JOIN Patient p ON a.patient_id = p.patient_id
                GROUP BY p.full_name
                HAVING SUM(b.total_amount) > 0
                ORDER BY total_billed DESC
            """,
            "staff_with_roles": """
                SELECT s.staff_id, s.name, s.email, s.salary,
                       CASE 
                           WHEN d.staff_id IS NOT NULL THEN 'Dentist - ' || d.specialization
                           WHEN da.staff_id IS NOT NULL THEN 'Dental Assistant'
                           WHEN r.staff_id IS NOT NULL THEN 'Receptionist'
                           ELSE 'Unknown'
                       END AS role
                FROM Staff s
                LEFT JOIN Dentist d ON s.staff_id = d.staff_id
                LEFT JOIN Dental_Assistant da ON s.staff_id = da.staff_id
                LEFT JOIN Receptionist r ON s.staff_id = r.staff_id
                ORDER BY s.name
            """,
            "appointments_with_staff": """
                SELECT a.appointment_id, p.full_name AS patient, 
                       a.appointment_datetime, a.status,
                       GROUP_CONCAT(s.name, ', ') AS staff_assigned
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                LEFT JOIN Appointment_Staff ast ON a.appointment_id = ast.appointment_id
                LEFT JOIN Staff s ON ast.staff_id = s.staff_id
                GROUP BY a.appointment_id, p.full_name, a.appointment_datetime, a.status
                ORDER BY a.appointment_datetime DESC
            """,
            "inventory_usage_report": """
                SELECT i.item_name, i.quantity AS current_stock,
                       COALESCE(SUM(dai.quantity_used), 0) AS total_used,
                       COUNT(DISTINCT dai.dental_action_id) AS times_used
                FROM Inventory i
                LEFT JOIN DentalAction_Inventory dai ON i.item_id = dai.item_id
                GROUP BY i.item_id, i.item_name, i.quantity
                ORDER BY total_used DESC
            """
        }
        return queries.get(query_key, "SELECT 1")
    
    def get_schema_info(self):
        if not self.cursor:
            return "Database not connected"
            
        try:
            schema_info = "=" * 80 + "\n"
            schema_info += "DATABASE SCHEMA - DENTAL CLINIC MANAGEMENT SYSTEM\n"
            schema_info += "=" * 80 + "\n\n"
            
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = self.cursor.fetchall()
            
            schema_info += f"Total Tables: {len(tables)}\n\n"
            
            for table in tables:
                table_name = table[0]
                schema_info += f"TABLE: {table_name}\n"
                schema_info += "-" * 80 + "\n"
                
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                columns = self.cursor.fetchall()
                
                schema_info += f"{'Column Name':<25} {'Type':<15} {'Constraints':<20}\n"
                schema_info += "-" * 80 + "\n"
                
                for col in columns:
                    col_name, col_type, not_null, default_val, pk = col[1], col[2], col[3], col[4], col[5]
                    constraints = []
                    if pk:
                        constraints.append("PRIMARY KEY")
                    if not_null:
                        constraints.append("NOT NULL")
                    
                    constraint_str = ", ".join(constraints) if constraints else ""
                    schema_info += f"{col_name:<25} {col_type:<15} {constraint_str:<20}\n"
                
                # Get row count
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = self.cursor.fetchone()[0]
                schema_info += f"\nTotal Rows: {row_count}\n"
                schema_info += "\n\n"
            
            return schema_info
        except Exception as e:
            return f"Error retrieving schema: {str(e)}"
    
    def get_table_count(self, table_name):
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return self.cursor.fetchone()[0]
        except:
            return 0
    
    def test_connection(self):
        try:
            self.cursor.execute("SELECT 1")
            messagebox.showinfo("Connection Test", "✅ Database connection is working properly!")
            self.connection_status.config(text="✅ Database connected")
        except Exception as e:
            messagebox.showerror("Connection Test", f"❌ Connection failed: {str(e)}")
            self.connection_status.config(text="❌ Connection failed")
    
    def reset_database(self):
        if messagebox.askyesno("Confirm Reset", "This will drop all tables and recreate them with sample data.\n\nAre you sure?"):
            try:
                self.drop_tables()
                
                # Re-create tables using LoginWindow methods
                login = LoginWindow(tk.Tk())
                login.cursor = self.cursor
                login.connection = self.connection
                login.create_tables()
                login.populate_tables()
                
                self.update_dashboard_stats()
                self.populate_table_list()
                self.refresh_schema()
                messagebox.showinfo("Success", "Database has been reset successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset database: {str(e)}")
    
    def update_connection_status(self, message):
        self.connection_status.config(text=message)
    
    def drop_tables(self):
        tables = [
            'Bill',
            'DentalAction_Inventory',
            'Inventory',
            'Prescription',
            'Treatment',
            'Dental_Action',
            'Appointment_Staff',
            'Appointment',
            'Staff_Schedule',
            'Receptionist',
            'Dental_Assistant',
            'Dentist',
            'Staff',
            'Room',
            'Patient'
        ]
        
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        self.connection.commit()


def main():
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
