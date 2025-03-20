"""
TODO: check that cancel appointment is working
"""

from app.config import Config
from tabulate import tabulate
from database import db 


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

def confirm_payment():
    payment_reference = input("Enter payment reference to confirm: ").strip()

  
    payment_record = db.fetch_one("""
        SELECT payment_id, patient_id, amount, payment_status FROM payments WHERE paypal_transaction_id = %s
    """, (payment_reference,))

    if not payment_record:
        print("Invalid payment reference!")
        return

    payment_id, patient_id, amount, status = payment_record

    if status == "Completed":
        print("Payment has already been confirmed.")
        return

    db.execute("""
        UPDATE payments SET payment_status = 'Completed' WHERE paypal_transaction_id = %s
    """, (payment_reference,))

    print(f"Payment of ${amount} for Patient ID {patient_id} has been confirmed!")


def receptionist_portal():
    while True:
        print("\nWelcome to the Online Receptionist Portal.Choose an option:")
        print("""
        1. Schedule an Appointment
        2. Reschedule an Appointment
        3. Cancel an Appointment
        4. View Scheduled Appointments 
        5. Confirm Payments
        6. Exit
        """)

        try:
            m2_choice = int(input("Pick an option (1-6): "))
            actions = {
                1: schedule_appointment,
                2: reschedule_appointment,
                3: cancel_appointment,
                4: view_appointments,
                5: confirm_payment
            }

            if m2_choice in actions:
                actions[m2_choice]() 
            elif m2_choice == 6:
                confirm_exit = input("Are you sure you want to exit? (y/n): ").strip().lower()
                if confirm_exit == "y":
                    print("Exiting...")
                    break
            else:
                print("Invalid option. Please choose between 1-6.")

        except ValueError:
            print("Invalid choice! Please enter a number between 1 and 6.")

