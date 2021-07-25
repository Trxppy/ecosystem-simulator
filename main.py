# import modules
from classes.environment import *
from classes.plant import *

# startup file
version = 0.2
print("-- Ecosystem Simulator")
print("--- Developed by Matthew Grant")
print("---- Version " + str(version) + "\n")
program_active = True

# import organism data from file
def import_organism(data):
    # parse data
    organism = data.split(" ")
    organism_name = organism[0]
    organism_count = organism[1]
    # check plants
    f = open('user/plants.txt', "r")
    for line in f:
        this_organism = line.split(",")
        name = this_organism[0]
        if(name.lower() == organism_name.lower()):
            return ["plant", line + "," + organism_count]
    # check animals
    f = open('user/animals.txt', "r")
    for line in f:
        this_organism = line.split(",")
        name = this_organism[0]
        if(name.lower() == organism_name.lower()):
            return ["animal", line + "," + organism_count]
    return False
while(program_active):

    # constant variables
    env_size_min = 4
    env_size_max = 25
    simulation_runtime_max = 1000

    # initialize start conditions
    inputValid = False
    while(inputValid == False):
        # validate environment size
        print("ENVIRONMENT SETUP ACTIVE")
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

    inputValid = False
    while(inputValid == False):
        # validate simulation length
        print("\nPlease enter the length of the simulation:")
        simulation_runtime = input()
        if(simulation_runtime.isnumeric() == False):
            # check if number is an int
            print("Sorry! Simulation length must be an integer.")
        else:
            # more detailed checks
            simulation_runtime = int(simulation_runtime)
            if(simulation_runtime > simulation_runtime_max):
                print("Sorry! Simulation length cannot exceed {}".format(simulation_runtime_max))
            else:
                print("Enter 'Y' to confirm a simulation length of {}".format(simulation_runtime))
                confirm_input = input()
                if(confirm_input.lower() == 'y'):
                    inputValid = True
                

    # import organisms into the new environment
    plants = []
    animals = []
    print("\nIMPORT ORGANISMS")
    print("Please enter the name of the organism and its spawn count (ex: pine 4)")
    print("Enter 'DONE' to continue")
    looping = True
    while(looping):
        organism_found = False
        while(organism_found == False):
            data = input()
            if(data.lower() == 'done'):
                looping = False
                organism_found = True
            else:
                print("Enter 'Y' to confirm this import statement")
                confirm_input = input()
                if(confirm_input.lower() == 'y'):   
                    organism_name = data.split(" ")[0]
                    organism_count = data.split(" ")[1]
                    if(import_organism(data) != False):
                        organism_type = import_organism(data)[0]
                        organism = import_organism(data)[1]
                        organism_found = True
                        if(organism_type == "animal"):
                            animals.append(organism)
                        else:
                            plants.append(organism)
                    else:
                        print("Organism not found. Please re-enter the import statement:")
                else:
                    print("Please re-enter the import statement:")

    # handle simulation
    print("\n\nSIMULATION SETUP COMPLETE")
    setup_active = True
    while(setup_active):
        print("Please enter a command:")
        command = input()
        if(command == "run"):
            # run simulation
            env.simulate(simulation_runtime, plants, animals)
            print("\n")
        elif(command == "restart"):
            # restart simulation
            setup_active = False
        elif(command == "end"):
            # end simulation
            setup_active = False
            program_active = False
        elif(command == "help"):
            # view commands options
            print("run -> run simulation with given setup parameters")
            print("restart -> restart simulation with given setup parameters")
            print("end -> exit simulation")
            print("help -> view list of commands")
        else:
            # if invalid input detected
            print("INVALID COMMAND '{}'\n".format(command))


