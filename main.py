"""
Notes:
    The doctor's menu mainly consists of ways to view and change the database values.
    We should make the doctor's main menu 3 options, a current appointment option (Connects to the
    current patient and room and then manipulate or add values in the database based on the
    current appointment).
    Then The 2nd option should be to manipulate (as it currently is)
    and the third to exi to the main menu.
    This way when the doctor walks into the room, it is up and ready to use for the current
    patient, and they don't have to enter the patient id each time they need to make an
    addition or adjustment.
    And the doctor can still manipulate the database as needed.
"""
from doctors import *
from patients import patients_menu
from receptionist import *
from database import db 

def main_menu():
    while True:

        try:
            print("Welcome to the main portal.")
            print("""
                1. Receptionist portal
                2. Doctor portal
                3. Patient portal
                4. Exit
            """)
            menu_options = int(input("Pick an option (1-4):"))
            
            if menu_options == 1:
                receptionist_portal()
            elif menu_options == 2:
                doctor_menu() 

            elif menu_options == 3:
                patients_menu()

            elif menu_options == 4:
                print("Exiting the portal...")
                break
            else:
                print("Invalid option. Please choose between 1-4.") 

        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    try:
        main_menu()
    finally:
        print("Closing database connection..")
        db.close_connection()
