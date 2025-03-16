"""
TODO: check that cancel appointment is working
"""

import mysql.connector
from app.config import Config
from tabulate import tabulate

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        self.cursor = self.db.cursor()

    def close_connection(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("Connection Closed")

    def fetch_one(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.db.commit()

db = Database()

print("Database Host:", Config.DB_HOST)
print("Database User:", Config.DB_USER)
print("Database Name:", Config.DB_NAME)

def verify_patient():
    while True:
        patient_id = input("Enter Patient ID: ")
        patient = db.fetch_one("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        if patient:
            return patient_id  
        print("Error: Patient not found.")

def select_doctor():
    doctors = db.fetch_all("SELECT doctor_id, first_name, last_name, specialty FROM doctors")

    print("\nAvailable doctors:")
    for doc in doctors:
        print(f"ID: {doc[0]} | Name: {doc[1]} {doc[2]} | Specialty: {doc[3]}")

    while True:
        doctor_id = input("\nEnter Doctor ID: ")
        if db.fetch_one("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,)):
            return doctor_id  
        print("Error: Doctor not found.")

def get_appointment_details():
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter appointment time (HH:MM:SS): ")
    reason = input("Enter reason for visit: ")
    return appointment_date, appointment_time, reason

def check_doctor_availability(doctor_id, appointment_date, appointment_time):
    conflict = db.fetch_one("""
        SELECT * FROM appointments 
        WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
    """, (doctor_id, appointment_date, appointment_time))
    return not conflict

def schedule_appointment():
    patient_id = verify_patient()
    doctor_id = select_doctor()
    appointment_date, appointment_time, reason = get_appointment_details()

    if not check_doctor_availability(doctor_id, appointment_date, appointment_time):
        print("Error: The doctor is unavailable at this time. Please pick another time.")
        return

    db.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason_for_visit, 
        appointment_status)
        VALUES (%s, %s, %s, %s, %s, 'scheduled')
    """, (patient_id, doctor_id, appointment_date, appointment_time, reason))

    print("Appointment successfully scheduled.")

def reschedule_appointment():
    appointment_id = input("Enter the Appointment ID: ")
    if not db.fetch_one("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,)):
        print("Error: Appointment not found.")
        return

    #  Gathers from input instead of using the function
    #  No need to change reason if just being rescheduled
    new_date = input("Enter new appointment date: ")
    new_time = input("Enter new appointment time: ")

    db.execute("""
        UPDATE appointments 
        SET appointment_date = %s, appointment_time = %s, appointment_status = %s 
        WHERE appointment_id = %s
""", (new_date, new_time,  'scheduled', appointment_id))

    rescheduled_apt = db.fetch_all("""
        SELECT a.appointment_id, CONCAT(p.first_name,' ', p.last_name), CONCAT(d.first_name,' ', d.last_name), 
               a.appointment_date, a.appointment_time, a.reason_for_visit, a.appointment_status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_id = %s 
        ORDER BY a.appointment_date, a.appointment_time
    """, (appointment_id,))

    headers = ['Apt. ID', 'Patient Name', 'Doctor Name', 'Date', 'Time', 'Reason For Visit', 'Status']

    print("\nAppointment successfully rescheduled.")
    print(tabulate(rescheduled_apt, headers=headers, tablefmt='Grid'))

def cancel_appointment():
    appointment_id = input("Enter the Appointment ID to cancel: ")
    if not db.fetch_one("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,)):
        print("Error: Appointment not found.")
        return

    db.execute("UPDATE appointments SET status = 'canceled' WHERE appointment_id = %s", (appointment_id,))
    print("Appointment successfully canceled.")

def view_appointments():
# CHANGES: Cleaned up the output
# now using a table to display appointments
# used concat to connect patients first and last name, and doctors first and last name
    appointments = db.fetch_all("""
        SELECT a.appointment_id, CONCAT(p.first_name,' ', p.last_name), CONCAT(d.first_name,' ', d.last_name), 
               a.appointment_date, a.appointment_time, a.reason_for_visit, a.appointment_status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_status != 'completed'
        ORDER BY a.appointment_date, a.appointment_time
    """)

    if not appointments:
        print("No scheduled appointments found.")
        return

    headers = ['Apt. ID', 'Patient Name', 'Doctor Name', 'Date', 'Time', 'Reason For Visit', 'Status']
    print("\nAppointments:")
    print(tabulate(appointments, headers=headers, tablefmt='grid'))

def main_portal():
    while True:
        try:
            print(""" 
            Welcome to the Online Receptionist Portal. 

            1. Schedule an Appointment
            2. Reschedule an Appointment
            3. Cancel an Appointment
            4. View Scheduled Appointments
            5. Exit
            """)

            user_choice = int(input("Pick an option (1-5): "))   

            if user_choice == 1:
                schedule_appointment()
            elif user_choice == 2:
                reschedule_appointment()
                input("\nPress enter to continue: ")
            elif user_choice == 3:
                cancel_appointment()
            elif user_choice == 4:
                view_appointments()
                # Added this for better viewing of the appointments and returns to the main menu when enter is pressed
                input("\nPress enter for main menu: ")
                main_portal()
            elif user_choice == 5:
                print("Exiting the portal...")
                break
            else:
                print("Invalid option. Please choose between 1-5.")

        except ValueError:
            print("Invalid input. Please enter a number from 1-5.")

main_portal()

# Close connection
db.close_connection()
