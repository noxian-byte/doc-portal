
from receptionist import view_appointments

from main import db
from tabulate import tabulate

def view_patient_records():

    view_record = input("Enter patient ID to view records: ")

    patient_records = db.fetch_all("SELECT * FROM medical_records WHERE patient_id = %s", (view_record,))

    if patient_records:
        headers = ['record_id', 'patient_id', 'doctor_id', 'diagnosis', 'treatment', 'prescription',
                   'visit_date', 'notes']
        print(tabulate(patient_records, headers=headers, tablefmt='Grid'))

    else:
        print('No Records Found')

def update_medical_records():

    while True:
        try:
            view_p1 = int(input("Enter ID of patient: "))
            break 
        except ValueError:
            print("Invalid input! Please enter a valid patient ID.")


    patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (view_p1,))

    if patient_name_tuple:
        patient_name = patient_name_tuple[0]
    else:
        print(f"No patient found with ID {view_p1}. Please check the ID and try again.")
        return
    
    # view_p1 = input("Enter ID of patient: ")

    # patient_name_tuple = db.fetch_one("SELECT first_name FROM patients WHERE patient_id = %s", (view_p1,))
    
    # if patient_name_tuple:
    #     patient_name = patient_name_tuple[0]  # fetch_one(tuple)
    # else:
    #     print("Patient not found.")
    #     return

    while True: 
        try: 
            print("""
            1. Update Diagnosis
            2. Update Treatment
            3. Update Prescription
            4. Update Doctor's note
            """)
            

            update_options = int(input("Pick an option (1-4):"))

            if update_options in [1, 2, 3, 4]:
                break  
            else:
                print("Invalid option! Please choose between 1-4.")
        except ValueError:
            print("Invalid input! Please enter an integer between 1 and 4.")

    if update_options == 1:
        
        diag_update = db.fetch_one("SELECT diagnosis FROM medical_records WHERE patient_id = %s", (view_p1,))
        
        if diag_update:
            print(f"Here is the old diagnosis of Patient {patient_name}: {diag_update[0]}")  
            diagnosis_update = input("Enter new diagnosis: ")

          
            db.execute("""
            UPDATE medical_records
            SET diagnosis = %s
            WHERE patient_id = %s
            """, (diagnosis_update, view_p1))
            
            print(f"Patient {patient_name} with ID ({view_p1}), now has a new diagnosis: {diagnosis_update}")

    elif update_options == 2:
        
        treatment_update = db.fetch_one("SELECT treatment FROM medical_records WHERE patient_id = %s", (view_p1,))
        
        if treatment_update:
            print(f"Here is the old treatment of Patient {patient_name}: {treatment_update[0]}")  
            treat_update = input("Enter new treatment: ")

          
            db.execute("""
            UPDATE medical_records
            SET treatment = %s
            WHERE patient_id = %s
            """, (treat_update, view_p1))
            
            print(f"Patient {patient_name} with ID ({view_p1}), now has a new treatment: {treat_update}")

    elif update_options == 3:
       
        prescription_update = db.fetch_one("SELECT prescription FROM medical_records WHERE patient_id = %s", (view_p1,))
        
        if prescription_update:
            print(f"Here is the old prescription of Patient {patient_name}: {prescription_update[0]}")  
            prescription_new = input("Enter new prescription: ")

          
            db.execute("""
            UPDATE medical_records
            SET prescription = %s
            WHERE patient_id = %s
            """, (prescription_new, view_p1))
            
            print(f"Patient {patient_name} with ID ({view_p1}), now has a new prescription: {prescription_new}")

    elif update_options == 4:
       
        doctor_note_update = db.fetch_one("SELECT doctor_note FROM medical_records WHERE patient_id = %s", (view_p1,))
        
        if doctor_note_update:
            print(f"Here is the old doctor's note of Patient {patient_name}: {doctor_note_update[0]}") 
            doctor_note_new = input("Enter new doctor's note: ")

            db.execute("""
            UPDATE medical_records
            SET doctor_note = %s
            WHERE patient_id = %s
            """, (doctor_note_new, view_p1))
            
            print(f"Patient {patient_name} with ID ({view_p1}), now has a new doctor's note: {doctor_note_new}")

    else:
        print("Invalid option. Please choose between 1-4.")

def generate_prescriptions():

    view_patientid = input("Enter patient ID: ")

    view_prescriptions = db.fetch_all("""
    SELECT prescription, patient_id FROM medical_records WHERE patient_id = %s
    """, (view_patientid,))

    headers = ['Patient ID', 'Prescription']

    if view_prescriptions:
        print(f"\nThis is the prescription that belongs to the patient with ID {view_patientid}.")
        print(tabulate(view_prescriptions, headers=headers, tablefmt='grid'))
    else:
        print(f"No prescriptions found for patient with ID {view_patientid}.")



def doctor_menu():
    while True:
        try:
            print("Welcome doctor.")
            print("""
                1. View Patient Appointments 
                2. View Patient Records
                3. Update Medical Records 
                4. Generate Prescriptions 
                5. View Lab Reports
                6. Write Notes & Recommendations 
                7. Exit
            """)
            m2_choice = int(input("Pick an option (1-7):"))

            if m2_choice == 1:
                view_appointments()
                input("Press enter to continue")
            elif m2_choice == 2:
                view_patient_records()
                input("Press Enter to Continue")
            elif m2_choice == 3:
                update_medical_records()
                input("Press Enter to Continue")
            elif m2_choice == 4:
                generate_prescriptions()
                input("Press Enter to Continue")
            elif m2_choice == 5:
                pass

            elif m2_choice == 6:
                pass

            elif m2_choice == 7:
                print("Exiting...")
                break

            else:
                print("Invalid option. Please choose between 1-7.") 

        except ValueError:
            print("Invalid choice.")

#  doctor_menu()
