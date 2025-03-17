
from receptionist import view_appointments
from queries import *
import main
from tabulate import tabulate
from database import db 

def view_patient_records():

    view_record = input("Enter patient ID to view records: ")

    patient_records = db.fetch_all(GET_PATIENT_RECORDS, (view_record,))

    if patient_records:
        headers = ['record_id', 'patient_id', 'doctor_id', 'diagnosis', 'treatment', 'prescription',
                   'visit_date', 'notes']
        print(tabulate(patient_records, headers=headers, tablefmt='Grid'))

    else:
        print('No Records Found')
        print("Ensure the patient has been registered and their medical records are updated.")

def update_medical_records():
   
    while True:
        try:
            view_p1 = int(input("Enter ID of patient: "))
            break 
        except ValueError:
            print("Invalid input! Please enter a valid patient ID.")

   
    patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (view_p1,))
    if not patient_name_tuple:
        print(f"No patient found with ID {view_p1}. Please check the ID and try again.")
        return
    patient_name = patient_name_tuple[0]

    fields = {
        1: "diagnosis",
        2: "treatment",
        3: "prescription",
        4: "doctor_note"
    }

    print("""
    1. Update Diagnosis
    2. Update Treatment
    3. Update Prescription
    4. Update Doctor's note
    """)

    try:
        update_option = int(input("Pick an option (1-4): "))
        if update_option not in fields:
            print("Invalid option! Please choose between 1-4.")
            return
    except ValueError:
        print("Invalid input! Please enter a number between 1-4.")
        return

    field_name = fields[update_option]

  
    old_value = db.fetch_one(f"SELECT {field_name} FROM medical_records WHERE patient_id = %s", (view_p1,))
    if old_value:
        print(f"Here is the old {field_name} of Patient {patient_name}: {old_value[0]}")
    
    new_value = input(f"Enter new {field_name}: ").strip()
    if not new_value:
        print(f"{field_name.capitalize()} cannot be empty!")
        return

    
    db.execute(f"UPDATE medical_records SET {field_name} = %s WHERE patient_id = %s", (new_value, view_p1))
    print(f"Patient {patient_name} with ID {view_p1} now has a new {field_name}: {new_value}")



def generate_prescriptions():

    view_patientid = input("Enter patient ID: ")

    view_prescriptions = db.fetch_all(GET_PATIENT_PRESCRIPTION, (view_patientid,))

    headers = ['Patient ID', 'Prescription']

    if view_prescriptions:
        print(f"\nThis is the prescription that belongs to the patient with ID {view_patientid}.")
        print(tabulate(view_prescriptions, headers=headers, tablefmt='grid'))
    else:
        print(f"No prescriptions found for patient with ID {view_patientid}.")

def view_lab_reports():
    
    view_patientid = input("Enter patient ID: ")

    view_reports = db.fetch_all(GET_NOTES, (view_patientid,))

    headers = ['Patient ID', 'Lab Report']

    if view_reports:
        print(f"\nThis is the lab report of patient {view_patientid}: .")
        print(tabulate(view_reports, headers=headers, tablefmt='grid'))
    else:
        print(f"There is no lab report that was found for patient with ID: {view_patientid}.")

def write_notes():
    p1_choice = input("Enter patient ID: ")
    add_doc_notes = input("Enter notes/recommendations for patient: ")

  
    patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (p1_choice,))
    if not patient_name_tuple:
        print(f"No patient found with ID {p1_choice}. Please check the ID and try again.")
        return
    patient_name = patient_name_tuple[0]

    db.execute(UPDATE_DOCTOR_NOTE, (add_doc_notes, p1_choice))

    print(f"Notes added for Patient {patient_name} (ID: {p1_choice}): {add_doc_notes}")

def doctor_menu():
    while True:
        print("\nWelcome, Doctor. Choose an option:")
        print("""
        1. View Patient Appointments 
        2. View Patient Records
        3. Update Medical Records 
        4. Generate Prescriptions 
        5. View Lab Reports
        6. Write Notes & Recommendations 
        7. Exit
        """)

        try:
            m2_choice = int(input("Pick an option (1-7): "))
            actions = {
                1: view_appointments,
                2: view_patient_records,
                3: update_medical_records,
                4: generate_prescriptions,
                5: view_lab_reports,
                6: write_notes
            }

            if m2_choice in actions:
                actions[m2_choice]() 
            elif m2_choice == 7:
                confirm_exit = input("Are you sure you want to exit? (y/n): ").strip().lower()
                if confirm_exit == "y":
                    print("Exiting...")
                    break
            else:
                print("Invalid option. Please choose between 1-7.")

        except ValueError:
            print("Invalid choice! Please enter a number between 1 and 7.")


#  doctor_menu()
