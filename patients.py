# Started the patients.py file
# Just made a menu

def patients_menu():
    while True:
        try:
            print("\nWelcome to the Patients Portal\n"
                  """
                    1. option 1
                    2. option 2
                    3. option 3
                    4. Exit                   
                  """)
            user = int(input("Pick an option (1-4): "))
            if user == 1:
                pass
            elif user == 2:
                pass
            elif user == 3:
                pass
            elif user == 4:
                print("Exiting patients...")
                break
            else:
                print("error")
        except ValueError:
            print("Invalid Input")
