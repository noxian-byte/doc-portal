from receptionist import receptionist_portal
from doctors import doctor_menu



def main_menu():
    while True:
        try:
            print("Welcome to the doc-portal.")
            print("""
                1. Receptionist portal
                2. Doctor portal
                3. Patient portal
                4. Exit
            """)
            menu_options = int(input("Pick an option (1-4): "))
            
            if menu_options == 1:
                receptionist_portal()
            elif menu_options== 2:
                doctor_menu()

            elif menu_options == 3:
                pass

            elif menu_options == 4:
                print("Exiting the portal...")
                break
            else:
                print("Invalid option. Please choose between 1-4.") 

        except ValueError:
            print("Invalid input.")

main_menu()
