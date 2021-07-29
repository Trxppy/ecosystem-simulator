# import modules
from classes.environment import *
from classes.plant import *

# startup file
version = "0.2.0"
print("-- Ecosystem Simulator")
print("--- Developed by Matthew Grant")
print("---- Version " + str(version) + "\n")

# setup stages vars
program_active = True
environment_setup_active = True
organism_setup_active = True
menu_active = False

# import organism data from file
def import_organism(data):
    # parse data
    organism = data.split(" ")
    organism_name = organism[0]
    organism_count = organism[1]
    # check plants
    with open('user/plants.txt', "r") as f:
        for line in f:
            this_organism = json.loads(line)
            name = this_organism["species"]
            if(name.lower() == organism_name.lower()):
                return ["plant", line]
    # check animals
    with open('user/animals.txt', "r") as f:
        for line in f:
            this_organism = json.loads(line)
            name = this_organism["species"]
            if(name.lower() == organism_name.lower()):
                return ["animal", line]
        return False

def show_rename_menu():
    # handle organism rename
    print("\nPlease enter the name of the organism and the new desired name (ex: pine1 pine2)")
    data = input()
      # parse data
    organism = data.split(" ")
    organism_current_name = organism[0]
    organism_new_name = organism[1]
    # scan plant file
    organism_exists = True
    organisms = {}
    with open('user/plants.txt', "r") as f:
        # check plant save file for duplicate names
        for line in f:
            # make sure organism exists and isn't a duplicate
            data = json.loads(line)
            if(data["species"] == organism_new_name):
                print("Organism already exists. Please re-enter your statement with a different name:")
                return
            if(data["species"] == organism_current_name):
                organism_exists = True
        if(organism_exists == False):
            # return method if organism wasn't found in initial search
            print("ORGANISM NOT FOUND. PLEASE TRY AGAIN")
            return
        else:
            # otherwise, save data to temporary array (organisms)
            organisms[data["species"]] = data
    # rewrite plants file
    if(organism_exists):
        # update plant data for selected species
        organisms[organism_current_name]["species"] = organism_new_name # update species name
        with open('user/plants.txt', "w+") as f:
            for index in organisms:
                if(organisms[index]["parent"] == organism_current_name):
                    # update parent species name if it matches the selected species
                    organisms[index]["parent"] = organism_new_name
                f.write(json.dumps(organisms[index]) + "\n")
                

while(program_active):

    print("ENVIRONMENT SETUP ACTIVE")

    # constant variables
    env_size_min = 4
    env_size_max = 25
    simulation_runtime_max = 5000

    # initialize start conditions (environment setup)
    while(environment_setup_active):
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
                        environment_setup_active = False
                

    # import organisms into the new environment (organism setup)
    while(organism_setup_active):
        plants = []
        animals = []
        print("\nIMPORT ORGANISMS")
        print("Please enter the name of the organism and its spawn count (ex: pine 4)")
        print("Enter 'DONE' to continue")
        looping = True # for input validation
        while(looping): # input loop (user can continue to make entries until they opt out of the loop via "done" command)
            organism_found = False
            while(organism_found == False): # input validation
                data = input()
                if(data.lower() == 'done'):
                    looping = False
                    organism_setup_active = False
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
                                animals.append([organism, organism_count])
                            else:
                                plants.append([organism, organism_count])
                        else:
                            print("Organism not found. Please re-enter the import statement:")
                    else:
                        print("Please re-enter the import statement:")

    # handle simulation
    print("\n\nSIMULATION SETUP COMPLETE")
    menu_active = True
    simulation_run = False
    while(menu_active):
        print("Please enter a command:")
        command = input()
        if(command == "run"):
            # run simulation
            env.simulate(simulation_runtime, plants, animals)
            simulation_run = True
            print("\n")
        elif(command == "restart"):
            # restart simulation
            menu_active = False
            environment_setup_active = True
            organism_setup_active = True
            print("\n")
        elif(command == "repopulate"):
            # repopulate simulation
            menu_active = False
            organism_setup_active = True
        elif(command == "rename"):
            # rename organisms
            show_rename_menu()
        elif(command == "merge"):
            # save and merge simulation data
            if(simulation_run):
                env.merge(simulation_runtime)
                print("\n")
            else:
                print("Please run simulation first!\n")
        elif(command == "end"):
            # end simulation
            menu_active = False # exit 
            program_active = False
        elif(command == "help"):
            # view commands options
            print("\nCOMMAND LIST:")
            print("run -> run simulation with given setup parameters")
            print("restart -> restart simulation with given setup parameters")
            print("repopulate -> re-enter starting organism parameters")
            print("rename -> rename all references of an organism")
            print("merge -> merge the organism data from previously run simulation into the global data")
            print("end -> exit simulation")
            print("help -> view list of commands")
            print("--------------------------------\n")
        else:
            # if invalid input detected
            print("INVALID COMMAND '{}'\n".format(command))


