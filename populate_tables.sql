--- Insert Patient
INSERT INTO Patient (patient_id, full_name, date_of_birth, street, city, province, postal_code, gender, phone, email, medical_history, insurance)
VALUES (1, 'John Doe', TO_DATE('2000-01-01', 'YYYY-MM-DD'), '123 Main st', 'Toronto', 'ON', 'M5V1E3', 'Male', '647-123-1234', 'john.doe@email.com', 'No known allergies', 'SunLife: 1234567890');
INSERT INTO Patient (patient_id, full_name, date_of_birth, street, city, province, postal_code, gender, phone, email, medical_history, insurance) 
VALUES (2,'Bob Smith',to_date('85-02-20','RR-MM-DD'),'45 King St','Toronto','ON','M5V2B2','Male','416-222-3333','bob@example.com','Diabetic','Manulife');
INSERT INTO Patient (patient_id, full_name, date_of_birth, street, city, province, postal_code, gender, phone, email, medical_history, insurance)
VALUES (3,'Charlie Brown',to_date('00-10-15','RR-MM-DD'),'78 Queen St','Ottawa','ON','K1A0B1','Male','613-111-2222','charlie@example.com','None','BlueCross');
INSERT INTO Patient (patient_id, full_name, date_of_birth, street, city, province, postal_code, gender, phone, email, medical_history, insurance)
VALUES (4,'Diana Prince',to_date('95-07-01','RR-MM-DD'),'9 Bloor St','Mississauga','ON','L5B4C3','Female','905-444-5555','diana@example.com','Asthma','SunLife');
INSERT INTO Patient (patient_id, full_name, date_of_birth, street, city, province, postal_code, gender, phone, email, medical_history, insurance)
VALUES (5,'Ethan Hunt',to_date('78-12-25','RR-MM-DD'),'55 Bay St','Toronto','ON','M5J2X1','Male','416-777-8888','ethan@example.com','High blood pressure','GreatWest');

--- Insert Room
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (100, 'Surgery', 1, 'Y');
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (101, 'Consultation', 1, 'Y');
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (102, 'Surgery', 2, 'Y');
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (103, 'X-Ray', 1, 'N');
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (104, 'Hygiene', 1, 'Y');
INSERT INTO Room (room_number, room_type, capacity, availability) VALUES (105, 'Checkup', 1, 'Y');

--- Insert Appointment
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1000, 1, 100, to_timestamp('2025-09-25 09:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'SCHEDULED');
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1001, 1, 101, to_timestamp('2025-09-25 09:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'SCHEDULED');
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1002, 2, 102, to_timestamp('2025-09-25 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'COMPLETED');
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1003, 3, 103, to_timestamp('2025-09-26 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'SCHEDULED');
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1004, 4, 104, to_timestamp('2025-09-27 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'CANCELLED');
INSERT INTO Appointment (appointment_id, patient_id, room_number, appointment_datetime, status)
VALUES (1005, 5, 105, to_timestamp('2025-09-28 15:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'SCHEDULED');

--- Insert Staff
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (200, 'Dr. Alice Brown', '416-111-1111', 'alice.brown@gmail.com', 90000.00);
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (201, 'Dr. John Miller', '416-999-1111', 'john.miller@example.com', 120000.00);
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (202, 'Dr. Sarah White', '416-999-2222', 'sarah.white@example.com', 115000.00);
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (203, 'Emily Davis', '416-999-3333', 'emily.davis@example.com', 55000.00);
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (204, 'Mark Wilson', '416-999-4444', 'mark.wilson@example.com', 40000.00);
INSERT INTO Staff (staff_id, name, phone, email, salary) VALUES (205, 'Anna Brown', '416-999-5555', 'anna.brown@example.com', 42000.00);

--- Insert Staff Schedule
INSERT INTO Staff_Schedule (schedule_id, staff_id, start_time, end_time) VALUES (301, 201, to_timestamp('2025-09-25 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), to_timestamp('2025-09-25 17:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO Staff_Schedule (schedule_id, staff_id, start_time, end_time) VALUES (302, 202, to_timestamp('2025-09-25 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), to_timestamp('2025-09-25 18:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO Staff_Schedule (schedule_id, staff_id, start_time, end_time) VALUES (303, 203, to_timestamp('2025-09-25 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), to_timestamp('2025-09-25 13:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO Staff_Schedule (schedule_id, staff_id, start_time, end_time) VALUES (304, 204, to_timestamp('2025-09-25 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), to_timestamp('2025-09-25 20:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO Staff_Schedule (schedule_id, staff_id, start_time, end_time) VALUES (305, 205, to_timestamp('2025-09-25 08:00:00', 'YYYY-MM-DD HH24:MI:SS'), to_timestamp('2025-09-25 16:00:00', 'YYYY-MM-DD HH24:MI:SS'));

--- Insert Dentist
INSERT INTO Dentist (staff_id, license_no, specialization) VALUES (200, '12345', 'Orthodontics');
INSERT INTO Dentist (staff_id, license_no, specialization) VALUES (201, 'LIC12345', 'Orthodontics');
INSERT INTO Dentist (staff_id, license_no, specialization) values (202, 'LIC67890', 'Endodontics');

-- Insert Dental Assistant
INSERT INTO Dental_Assistant (staff_id, certification) VALUES (203, 'Certified Dental Assistant Level II');

-- Insert Receptionist
INSERT INTO Receptionist (staff_id) values (204);
INSERT INTO Receptionist (staff_id) values (205);

-- Insert Appointment to Staff Link
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1000, 200);
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1001, 201);
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1001, 203);
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1002, 202);
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1003, 201);
INSERT INTO Appointment_Staff (appointment_id, staff_id) VALUES (1004, 202);

-- Insert Dental Actions
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (400, 1000, 100.00);
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (401, 1001, 200.00);
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (402, 1002, 500.00);
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (403, 1003, 100.00);
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (404, 1001, 300.00);
INSERT INTO Dental_Action (dental_action_id, appointment_id, cost) VALUES (405, 1005, 150.00);

-- Insert Treatment
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (500, 400, 'Root Canal', 'Surgery');
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (501, 401, 'Teeth cleaning', 'Hygiene');
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (502, 402, 'Root canal treatment', 'Surgery');
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (503, 403, 'Dental X-ray', 'Diagnostic');
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (504, 404, 'Tooth extraction', 'Surgery');
INSERT INTO Treatment (treatment_id, dental_action_id, description, type) VALUES (505, 405, 'Whitening treatment', 'Cosmetic');

-- Insert Prescription
INSERT INTO Prescription (prescription_id, dental_action_id, medication, dosage, duration) VALUES (601, 402, 'Amoxicillin', '500mg', '7 days');
INSERT INTO Prescription (prescription_id, dental_action_id, medication, dosage, duration) VALUES (602, 402, 'Ibuprofen', '200mg', '5 days');
INSERT INTO Prescription (prescription_id, dental_action_id, medication, dosage, duration) VALUES (603, 404, 'Paracetamol', '500mg', '3 days');
INSERT INTO Prescription (prescription_id, dental_action_id, medication, dosage, duration) VALUES (604, 405, 'Mouthwash', '10ml', '14 days');
INSERT INTO Prescription (prescription_id, dental_action_id, medication, dosage, duration) VALUES (605, 401, 'Vitamin D', '1000 IU', '30 days');

-- Insert Inventory
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (700, 'Needles', 500, 'DentalSupplyCo');
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (701, 'Gloves', 200, 'DentalSupplies Inc');
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (702, 'Anesthetic', 50, 'HealthCorp');
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (703, 'X-Ray Film', 30, 'MedEquip Ltd');
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (704, 'Toothpaste', 100, 'DentalCare Co');
INSERT INTO Inventory (item_id, item_name, quantity, supplier) VALUES (705, 'Whitening Gel', 20, 'SmileTech');

-- Insert DentalAction to Inventory Link
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (400, 700, 2);
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (401, 701, 2);
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (402, 702, 1);
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (403, 703, 1);
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (404, 701, 1);
INSERT INTO DentalAction_Inventory (dental_action_id, item_id, quantity_used) VALUES (405, 705, 1);

-- Insert Bill
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (800, 400, 100.00, 'UNPAID', to_date('2025-09-25','YYYY-MM-DD'));
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (801, 401, 200.00, 'PAID', to_date('2025-09-25','YYYY-MM-DD'));
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (802, 402, 500.00, 'UNPAID', to_date('2025-09-25','YYYY-MM-DD'));
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (803, 403, 100.00, 'PARTIALLY_PAID', to_date('2025-09-26','YYYY-MM-DD'));
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (804, 404, 300.00, 'PAID', to_date('2025-09-27','YYYY-MM-DD'));
INSERT INTO Bill (bill_id, dental_action_id, total_amount, status, issue_date) VALUES (805, 405, 150.00, 'UNPAID', to_date('2025-09-28','YYYY-MM-DD'));

