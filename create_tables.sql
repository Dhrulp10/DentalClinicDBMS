CREATE TABLE Patient (
    patient_id INT PRIMARY KEY,
    full_name VARCHAR2(100) NOT NULL,
    date_of_birth DATE,
    street VARCHAR2(100),
    city VARCHAR2(20),
    province VARCHAR2(20),
    postal_code VARCHAR2(6),
    gender VARCHAR2(10),
    phone VARCHAR2(20),
    email VARCHAR2(100) UNIQUE,
    medical_history VARCHAR2(500),
    insurance VARCHAR2(100)
);

CREATE TABLE Room (
    room_number INT PRIMARY KEY,
    room_type VARCHAR2(50),
    capacity INT DEFAULT 0,
    availability CHAR(1) DEFAULT 'Y' CHECK (availability IN ('Y', 'N'))
);

CREATE TABLE Appointment (
    appointment_id INT PRIMARY KEY,
    patient_id INT NOT NULL,
    room_number INT NOT NULL,
    appointment_datetime TIMESTAMP NOT NULL,
    status VARCHAR2(10) DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'COMPLETED', 'CANCELLED')),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (room_number) REFERENCES Room(room_number)
);

CREATE TABLE Staff (
    staff_id INT PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    phone VARCHAR2(20),
    email VARCHAR2(100),
    salary DECIMAL(10, 2)
);

CREATE TABLE Staff_Schedule (
    schedule_id INT PRIMARY KEY,
    staff_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Dentist (
    staff_id INT PRIMARY KEY,
    license_no VARCHAR2(50),
    specialization VARCHAR2(100),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Dental_Assistant (
    staff_id INT PRIMARY KEY,
    certification VARCHAR2(100),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Receptionist (
    staff_id INT PRIMARY KEY,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Appointment_Staff (
    appointment_id INT NOT NULL,
    staff_id INT NOT NULL,
    PRIMARY KEY (appointment_id, staff_id),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

CREATE TABLE Dental_Action (
    dental_action_id INT PRIMARY KEY,
    appointment_id INT NOT NULL,
    cost DECIMAL(10, 2),
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE Treatment (
    treatment_id INT PRIMARY KEY,
    dental_action_id INT NOT NULL,
    description VARCHAR2(500),
    type VARCHAR2(50),
    FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
);

CREATE TABLE Prescription (
    prescription_id INT PRIMARY KEY,
    dental_action_id INT NOT NULL,
    medication VARCHAR2(100) NOT NULL,
    dosage VARCHAR2(50),
    duration VARCHAR2(50),
    FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
);

CREATE TABLE Inventory (
    item_id INT PRIMARY KEY,
    item_name VARCHAR2(100) NOT NULL, 
    quantity INT NOT NULL,
    supplier VARCHAR2(100)
);

CREATE TABLE DentalAction_Inventory (
    dental_action_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_used INT NOT NULL,
    PRIMARY KEY (dental_action_id, item_id),
    FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id),
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id)
);

CREATE TABLE Bill (
    bill_id INT PRIMARY KEY,
    dental_action_id INT NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR2(20) DEFAULT 'UNPAID' CHECK (status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID')),
    issue_date DATE,
    FOREIGN KEY (dental_action_id) REFERENCES Dental_Action(dental_action_id)
);
  