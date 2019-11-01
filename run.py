#python imports
import os
import signal
import sys
import time
from multiprocessing import Process

#project imports
from groundstation.station import Groundstation
from simulation.simulation import Simulation

groundstation = Groundstation()  
simulation = Simulation()       

def terminate_program():
    os.system("sudo service apache2 stop")       
    groundstation.terminate()
    simulation.terminate()
    sys.exit(0)    

def signal_handler(sig, frame):
    print("\nCtrl+C presses. Terminating the program\n")
    terminate_program()

def update_components():
    error_code = os.system("pip3 --version")
    # if pip is missing lets install it first
    if not error_code:
        os.system("sudo apt install python3-pip")

    error_code = os.system("sudo pip3 install -r requirements.txt")
    if not error_code:
        print("Unable to retrieve requirements for the simulator.\n" +
              "Correct your requirements.txt and try again later.\n")

def check_and_run():   
    error_code = os.system("service apache2 status")
    if error_code:
        os.system("sudo service apache2 start")      

    simulation.run()
    groundstation.run()

def show_initial_menu():
    terminate = False
    acceptable_input = [1,2,3]

    while not terminate:
        user_input = input("Welcome to the space simulator control centre\n" +
                            "What do you feel like doing:\n" +
                            "1) Check for udpates\n" +
                            "2) Run the application\n" +
                            "3) Terminate and close the app\n")
        try:       
            user_input = int(user_input)             
            if(user_input in acceptable_input):
                if(user_input == 1):
                    update_components()
                elif(user_input == 2):
                    signal.signal(signal.SIGINT, signal_handler)
                    check_and_run()
                else:  
                    terminate_program()  
                    terminate = True
        except ValueError:
            print("invalid input, please select number in range from 1 to 3\n")        

if __name__ == "__main__":
    show_initial_menu()