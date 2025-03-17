from database import db 
from queries import *
from tabulate import tabulate
from receptionist import *

def patient_appointments(patient_ID):

    view_all_appointments = db.fetchall(GET_PATIENT_APPOINTMENTS, (patient_ID))

    headers = ['Appointment Id', 'Patient ID', 'Doctor ID', 'Appointment Date', 'Appointment Time', 'Reason for visit', 'Status']

    if view_all_appointments:
        print(tabulate(view_all_appointments, headers=headers, tablefmt='grid'))
    else:
        print(f"You do not have any scheduled appointments.")

        apt_option = input("Would you like to schedule an appointment? (y/n)").lower()

        if apt_option == y:
            book_appointment()
        

def access_records(patient_ID):
     
    patient_records = db.fetchall(GET_PATIENT_RECORDS,(patient_ID))
    
    headers = ['Record Id', 'Patient ID', 'Doctor ID', 'Diagnosis', 'Treatment', 'Prescription', 'Visit date', 'Doctors Notes']

    if patient_records:
        print(tabulate(patient_records, headers=headers, tablefmt='grid'))
    else:
        print(f"Your file does not have any medical records on it.Please consult with your doctor") #add doc name later


def request_prescription():

    patient_prescription = input("What prescription would you like to put in a request for? ")

    # add patient request to a new table

def patient_report(patient_ID):

    view_reports = db.fetch_all(GET_NOTES, (patient_ID,))

    headers = ['Patient ID', 'Lab Report']

    if view_reports:
        print(f"\nThis is your lab report: .") # add patient name
        print(tabulate(view_reports, headers=headers, tablefmt='grid'))
    else:
        print(f"You currently do not have a lab report.")

# def pay_bills():
    #will add to it

def give_feedback(patient_ID):
    while True:
        
        recipient = input("Who would you like to give feedback to? (doctor/receptionist): ").strip().lower()

        if recipient not in ["doctor", "receptionist"]:
            print("Invalid choice! Please enter 'doctor' or 'receptionist'.")
            continue  

        feedback_text = input(f"Enter your feedback for the {recipient}: ").strip()

        if not feedback_text:
            print("Feedback cannot be empty! Please enter your feedback.")
            continue

      # table to be added
        db.execute("""
            INSERT INTO feedback (patient_id, recipient, feedback_text)
            VALUES (%s, %s, %s)
        """, (patient_ID, recipient, feedback_text))

        print("Thank you for your feedback! It has been submitted successfully.")

        more_feedback = input("Would you like to submit more feedback? (yes/no): ").strip().lower()
        if more_feedback != "yes":
            break  

def patient_menu():

    while True:
        patient_ID = input("Enter your Health ID: ").strip()

      
        patient_exists = db.fetch_one(GET_PATIENT_ID, (patient_ID,))
        
        if patient_exists:
            break  
        else:
            print("Invalid Health ID. Please try again.")

    while True:
        print("\nWelcome, Patient. Choose an option:")
        print("""
        1. View Appointments 
        2. Access Medical Records
        3. Book Appointment
        4. Cancel Appointment
        5. Request Prescriptions 
        6. View Lab Reports
        7. Pay Bills 
        8. Give Feedback 
        9. Exit
        """)

        try:
            m2_choice = int(input("Pick an option (1-9): "))
            actions = {
                1: patient_appointments,
                2: access_records,
                3: schedule_appointment,
                4: cancel_appointment,
                5: request_prescription,
                6: patient_report,
                7: pay_bills,
                8: give_feedback
            }

            if m2_choice in actions:
                actions[m2_choice]() 
            elif m2_choice == 9:
                confirm_exit = input("Are you sure you want to exit? (y/n): ").strip().lower()
                if confirm_exit == "y":
                    print("Exiting...")
                    break
            else:
                print("Invalid option. Please choose between 1-9.")

        except ValueError:
            print("Invalid choice! Please enter a number between 1 and 9.")

     


