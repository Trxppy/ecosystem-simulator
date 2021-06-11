# import modules
from classes.environment import *

# startup file
version = 0.1
print("-- Ecosystem Simulator")
print("--- Developed by Matthew Grant")
print("---- Version " + str(version) + "\n")

# constant variables
env_size_min = 4
env_size_max = 25

# initialize start conditions
inputValid = False
while(inputValid == False):
    # validate environment size
    print("\nPlease enter the size of the environment:")
    env_size = input()
    if(env_size.isnumeric() == False):
        # check if number is an int
        print("Sorry! Environment size must be an integer.")
    else:
        # more detailed checks
        env_size = int(env_size)
        if(env_size < env_size_min):
            print("Sorry! Environment size must be at least " + str(env_size_min) + " ("+ str(env_size_min) + "x" + str(env_size_min) + ")")
        elif(env_size > env_size_max):
            print("Sorry! Environment size cannot exceed " + str(env_size_max) + " ("+ str(env_size_max) + "x" + str(env_size_max) + ")")
        else:
            print("Enter 'Y' to confirm an environment size of " + str(env_size) + " ("+ str(env_size) + "x" + str(env_size) + ")")
            confirm_input = input()
            if(confirm_input.lower() == 'y'):
                inputValid = True

inputValid = False
while(inputValid == False):
    # validate environment water percentage
    print("\nPlease enter the percentage of surface water in the environment (1-100):")
    env_water_percentage = input()
    if(env_water_percentage.isnumeric() == False):
        # check if number is an int
        print("Sorry! Environment water percentage must be an integer.")
    else:
        # more detailed checks
        env_water_percentage = int(env_water_percentage)
        if(env_water_percentage < 1):
            print("Sorry! Environment water percentage must be at least 1%")
        elif(env_water_percentage > 100):
            print("Sorry! Environment water percentage cannot exceed 100%")
        else:
            print("Enter 'Y' to confirm an environment water percentage of " + str(env_water_percentage) + "%")
            confirm_input = input()
            if(confirm_input.lower() == 'y'):
                inputValid = True

inputValid = False
while(inputValid == False):
    # validate environment water distribution
    print("\nPlease enter the environment's water distribution (1-100):")
    env_water_distribution = input()
    if(env_water_distribution.isnumeric() == False):
        # check if number is an int
        print("Sorry! Environment water distribution must be an integer.")
    else:
        # more detailed checks
        env_water_distribution = int(env_water_distribution)
        if(env_water_distribution < 1):
            print("Sorry! Environment water distribution must be at least 1%")
        elif(env_water_distribution > 100):
            print("Sorry! Environment water distribution cannot exceed 100%")
        else:
            print("Enter 'Y' to confirm an environment water distribution of " + str(env_water_distribution) + "%")
            confirm_input = input()
            if(confirm_input.lower() == 'y'):
                inputValid = True

inputValid = False
while(inputValid == False):
    # validate environment rainfall frequency
    print("\nPlease enter the environment's rainfall frequency (1-100):")
    env_rainfall_frequency = input()
    if(env_rainfall_frequency.isnumeric() == False):
        # check if number is an int
        print("Sorry! Environment rainfall frequency must be an integer.")
    else:
        # more detailed checks
        env_rainfall_frequency = int(env_rainfall_frequency)
        if(env_rainfall_frequency < 1):
            print("Sorry! Environment rainfall frequency must be at least 1%")
        elif(env_rainfall_frequency > 100):
            print("Sorry! Environment rainfall frequency cannot exceed 100%")
        else:
            print("Enter 'Y' to confirm an environment rainfall frequency of " + str(env_rainfall_frequency) + "%")
            confirm_input = input()
            if(confirm_input.lower() == 'y'):
                inputValid = True

# initialize environment object
env = Environment(env_size, env_water_percentage, env_water_distribution, env_rainfall_frequency)

