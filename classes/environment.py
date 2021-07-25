# import modules
import math
import random
import os, shutil
import json
from classes.block import *
from classes.plant import *
from classes.animal import *

class Environment:

    boundary_check_indexes = []

    # initialize environment
    def __init__(self, size, water_percentage, water_distribution, rainfall_frequency):

        # create board array
        self.env_tiles = [None] * (size * size)
        tile_index = 0
        for x in self.env_tiles:
            self.env_tiles[tile_index] = Block(tile_index)
            tile_index += 1
        # organisms
        self.env_plants = []
        self.env_animals = []
        # temporary storage for dead organisms
        self.dead_plants = []
        self.dead_animals = []
        # reassign variables
        self.env_size = size * size
        self.env_width = size
        self.env_water_percentage = water_percentage
        self.env_water_distribution = water_distribution
        self.env_rainfall_frequency = rainfall_frequency
        # generation variables
        self.env_water_clusters = 0
        # output (summary) data
        self.animal_species = {}
        self.plant_species = {}
        # clear output folder
        self.clear_output()
        # run generator method
        self.generate()

    # generate environment
    def generate(self, reset = False):
        # if reset parameter detected, reset gameboard array
        if(reset):
            tile_index = 0
            for x in self.env_tiles:
                self.env_tiles[tile_index].reset_terrain()
                tile_index += 1
        # calculate ideal number of clusters given user parameters
        water_clusters_max = math.ceil((self.env_size/30) * (self.env_water_distribution/100))
        water_blocks_max = math.ceil((self.env_water_percentage/100) * self.env_size)
        # if water percentage is greater than zero, ensure there's at least one cluster
        if(self.env_water_percentage > 0 and water_clusters_max == 0):
            water_clusters_max = 1

        self.log_output("---ENVIRONMENT GENERATION", "setup.txt") # debug
        self.log_output("maximum clusters allowed->{}".format(water_clusters_max), "setup.txt") # debug
        while(len(self.get_water_blocks()) < water_blocks_max):
            # select random tile as starting point for new cluster
            rand_index = random.randint(0, len(self.env_tiles)-1)
            current_tile = self.env_tiles[rand_index]
            cursor = rand_index # cursor to guide expansion of cluster
            self.log_output("start->{}".format(rand_index), "setup.txt") # debug
            if(current_tile.terrain_generated == False):
                # create starting point for cluster
                tile_depth = random.randint(3, 5)
                current_tile.set_terrain("water", tile_depth)
                current_tile.set_water_depth(tile_depth - 1)
                cluster_created = False
                # expand cluster
                while(cluster_created == False):
                    cluster_expansion_chance = random.randint(0, 100)
                    boundary_indexes = self.get_neighbor_blocks(cursor)
                    cluster_size = math.floor(random.randint(math.ceil(self.env_size * 0.25), math.ceil(self.env_size * 0.75)) * (5/self.env_water_distribution))
                    if(cluster_size > self.env_size):
                        # ensure cluster is not larger than its environment
                        cluster_size = math.floor(random.randint(math.ceil(self.env_size * 0.25), math.ceil(self.env_size * 0.75)) * (1/self.env_water_distribution))
                    # chance of expansion is dependent on user parameter "env_water_percentage"; 100% water translates to 100% chance of cluster expanding
                    if(cluster_expansion_chance <= self.env_water_percentage):
                        for x in boundary_indexes:
                            self.log_output("testing block {}".format(x), "setup.txt") # debug
                            if(self.check_tile_boundary(x)):
                                if(self.env_tiles[x].terrain_generated == False):
                                    if(len(self.get_water_blocks()) < water_blocks_max):
                                        layer_height = random.randint(3, 5)
                                        self.expand_water_cluster(x, layer_height, water_blocks_max) # loop until cluster is created
                                        self.log_output("index->{}".format(x), "setup.txt") # debug
                                        self.env_tiles[x].set_terrain("water", layer_height)
                                        self.env_tiles[x].set_water_depth(layer_height - 1)
                        # if no expansion possible, break loop
                        self.log_output("endpoint->root method, no expansion possible (exhausted all boundaries)", "setup.txt") # debug
                        cluster_created = True
                    else:
                        # if no expansion possible, break loop
                        self.log_output("endpoint->root method, no expansion possible (low chance of expansion due to water percentage in environment)", "setup.txt") # debug
                        cluster_created = True
        # if insufficient water tiles created, recall generator
        if(len(self.get_water_blocks()) != water_blocks_max):
          self.generate(True)
        # generate water clusters
        self.generate_water_clusters(water_clusters_max)

    # expand water cluster around specific block (recursive)
    def expand_water_cluster(self, index, height, global_max):
        cluster_expansion_chance = random.randint(0, 100)
        boundary_indexes = self.get_neighbor_blocks(index)
         # chance of expansion is dependent on user parameter "env_water_percentage"; 100% water translates to 100% chance of cluster expanding
        if(cluster_expansion_chance <= self.env_water_percentage):
            for x in boundary_indexes:
                self.log_output("testing boundary block {} (original block->{})".format(x, index), "setup.txt") # debug
                if(self.check_tile_boundary(x)):
                    if(self.env_tiles[x].terrain_generated == False):
                        if(len(self.get_water_blocks()) < global_max):
                            self.log_output("sub-index->{}".format(x), "setup.txt") # debug
                            new_height = height - 1
                            if(new_height < 1):
                                new_height = 1
                            self.expand_water_cluster(x, new_height, global_max)
                            self.env_tiles[x].set_terrain("water", random.randint(3, 5))
                            self.log_output("current blocks:{}, max:{}".format(len(self.get_water_blocks()), max), "setup.txt") # debug
                            break
                        else:
                            break
            # if no expansion possible, break loop
            self.log_output("endpoint->root method, no expansion possible (exhausted all boundaries)", "setup.txt") # debug
            cluster_created = True
        else:
            self.log_output("endpoint->recursive method, no expansion possible (low chance of expansion due to water percentage in environment)", "setup.txt") # debug
            cluster_created = True

    # generate water clusters
    def generate_water_clusters(self, water_clusters_max):
        water_clusters_created = 1
        current_cluster = []
        unclustered_water_blocks = self.get_water_blocks()
        target_cluster_size = random.randint(math.ceil((len(self.get_water_blocks())/water_clusters_max) * 0.7), math.ceil((len(self.get_water_blocks())/water_clusters_max) * 1.3))
        while(len(unclustered_water_blocks) > 0):
            # cycle through each water block that needs to be assigned
            for x in self.get_water_blocks():
                boundary_indexes = self.get_neighbor_blocks(x.index, True)
                # for each water block, check neighbors for potential clustermates
                for y in boundary_indexes:
                    if(self.check_tile_boundary(y) and y not in current_cluster and self.get_block(y) in unclustered_water_blocks):
                        self.get_block(y).set_cluster("water",water_clusters_created)
                        current_cluster.append(y)
                        unclustered_water_blocks.remove(self.get_block(y))
                        # if current cluster size equals target cluster size, create new cluster
                        self.log_output("current cluster size->{}, target size->{}".format(len(current_cluster), target_cluster_size), "setup.txt") # debug
                        if(len(current_cluster) == target_cluster_size):
                            water_clusters_created += 1
                            current_cluster = []
                            target_cluster_size = random.randint(math.ceil((len(self.get_water_blocks())/water_clusters_max) * 0.7), math.ceil((len(self.get_water_blocks())/water_clusters_max) * 1.3))
        self.log_output("target clusters->{}, created clusters->{}".format(water_clusters_max, water_clusters_created), "setup.txt") # debug

    # log simulation data to output file
    def log_output(self, line, location):
        with open('output/' + location, "a") as f:
            f.write(line + "\n")

    # delete contents of output folder
    def clear_output(self):
        folder = 'output/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            os.unlink(file_path)

    # generate summary to output after simulation
    def generate_summary(self):
        with open('output/summary.txt', "a") as f:
            # output animal data
            extant_organisms = []
            for key in self.animal_species:
                extant_organisms = []
                # check for extant organisms
                for x in self.env_animals:
                    if(x.species == key):
                        extant_organisms.append(x)
                # if extant organism found, collect averages
                if(extant_organisms > 0):
                    line = "Species->{}, Avg. Max Size->{}".format(sum(organism.max_size for organism in extant_organisms))
                else:
                    line = "Species->{}, NO DATA (EXTINCT, WILL BE ADDED IN FUTURE UPDATE)".format(key)
            f.write(line + "\n")

    # check if tile exists
    def check_tile_boundary(self, index):
        if(index > self.env_size-1 or index < 0):
            return False
        else:
            return True

    # return all generated water blocks
    def get_water_blocks(self):
        blocks = []
        for x in self.env_tiles:
            if(x.terrain_type == "water"):
                blocks.append(x)
        return blocks

    # retrieve block given the index
    def get_block(self, index):
        for x in self.env_tiles:
            if(x.index == index):
                return x
        return None

    # retrieve plant object from specific block
    def get_plant(self, index):
        for x in self.env_plants:
            if(x.block_index == index):
                return x
        return False

    # retrieve index from random block (optional parameters can be included)
    def get_random_index(self, args=None):
        index = random.randint(0, self.env_size-1)
        if(args != None):
            conditions_met = 0
            while(conditions_met < len(args)):
                index = random.randint(0, self.env_size-1)
                block = self.get_block(index)
                if "terrain_type" in args:
                    # check for terrain type
                    if(block.terrain_type == args["terrain_type"]):
                        conditions_met += 1
                if "terrain_has_plant" in args:
                    # check for plant
                    if(block.terrain_has_plant == args["terrain_has_plant"]):
                        conditions_met += 1
                if "range" in args:
                    # check for custom range
                    if(block.index in args["range"]):
                        conditions_met += 1
        return index

    # retrieve indexes of neighboring blocks
    def get_neighbor_blocks(self, index, include_self=False):
        boundary_indexes = [index+1, index-1, index+self.env_width, index-self.env_width]
        if(include_self):
            boundary_indexes.append(index)
        random.shuffle(boundary_indexes)
        return boundary_indexes

    # retrive indexes of blocks within radius
    def get_radial_blocks(self, index, radius):
        radial_blocks = [index]
        radius = int(radius)
        upper_limit = index - ((((radius * 2) + 1) * ((radius * 2) + 1)-1)/2)
        lower_limit = index + (((radius * 2) + 1) * ((radius * 2) + 1)-1)
        cursor = upper_limit
        while(cursor < index):
            # cover blocks in upper portion of radial area 
            if(self.check_tile_boundary(cursor)):
                radial_blocks.append(cursor)
            cursor += 1
        cursor = index 
        while(cursor < lower_limit):
            # cover blocks in lower portion of radial area 
            if(self.check_tile_boundary(cursor)):
                radial_blocks.append(cursor)
            cursor += 1
        return radial_blocks

    # add variation to traits (used during reproduction)
    def variate_trait(self, baseline):
        trait = baseline
        variation_factor = random.choices(
            population=[-2, -1, 0, 1, 2], # -1->decrease, 0->remain the same (approx.), 1->increase
            weights=[0.05, 0.15, 0.6, 0.15, 0.05],
            k=1)[0]
        if(variation_factor == -2):
            # -2 -> moderately decrease trait
            trait = random.uniform(baseline * 0.6, baseline * 0.79)
        if(variation_factor == -1):
            # -1 -> slightly decrease trait
            trait = random.uniform(baseline * 0.8, baseline * 0.95)
        if(variation_factor == 0):
            # 0 -> keep trait around baseline
            trait = random.uniform(baseline * 0.96, baseline * 1.04)
        if(variation_factor == 1):
            # 1 -> slightly increase trait
            trait = random.uniform(baseline * 1.05, baseline * 1.2)
        if(variation_factor == 2):
            # 2 -> moderately increase trait
            trait = random.uniform(baseline * 1.21, baseline * 1.4)
        return round(trait, 2)       

    # find and gather suitable food
    def find_food(self, animal):
        index = animal.location
        movement = animal.movement
        food_type = animal.food_type.strip() # remove whitespace
        radius = math.ceil(movement * 3)
        boundary_indexes = self.get_radial_blocks(index, radius)
        for x in boundary_indexes:
            # adds environmental boundary for water-based organism
            if(self.get_block(x).terrain_type == animal.preferred_terrain or (animal.preferred_terrain != "water" and self.get_block(x).terrain_type == "water" and self.get_block(x).terrain_water_depth <= 1)):
                if(food_type == "herbivore" or food_type == "omnivore"):
                    # if herb/omnivore, check if block has plant
                    if(self.get_plant(x) != False):
                        # if plant found, check if plant has enough health to be eaten
                        if(self.get_plant(x).plant_health > 0 and animal.animal_food < animal.min_food):
                            animal.animal_food += 1
                            animal.animal_stomach.append(self.get_plant(x).species)
                            self.get_plant(x).plant_health -= 1
                if(food_type == "carnivore" or food_type == "omnivore"):
                    for y in self.get_block(x).terrain_dead_animals:
                        # check for dead animals first (read: easy meals); neglect prey size if larger
                        if(animal.animal_decay_tolerance <= y.animal_decay_index and animal.animal_consumable_meat > 0):
                            # make sure animal stomach can sufficiently process the decayed prey item
                            animal.animal_food += 2
                            animal.animal_consumable_meat -= 2
                            animal.animal_stomach.append(y.species)
                    # if carn/omnivore, check for smaller animals (half size at most) on block
                    for y in self.get_block(x).terrain_animals:
                        if(y.animal_size < animal.animal_size/2 and animal.animal_food < animal.min_food):
                            # remove prey from simulation
                            animal.animal_food += 2
                            animal.animal_consumable_meat -= 2
                            animal.animal_stomach.append(y.species)
                            y.animal_health -= y.animal_health_max

    # find and gather suitable water
    def find_water(self, animal):
        index = animal.location
        movement = animal.movement
        radius = math.ceil(movement * 3)
        boundary_indexes = self.get_radial_blocks(index, radius)
        for x in boundary_indexes:
            # check if block contains water
            block = self.get_block(x)
            if(block.terrain_type == "water" and animal.animal_water < animal.animal_thirst):
                # if water found, add to total
                animal.animal_water += 10
                animal.animal_thirst -= 10

    # find suitable mate for given animal
    def find_mate(self, animal):
        mate_found = False
        radius = math.ceil(animal.movement * 3)
        index = animal.location
        boundary_indexes = self.get_radial_blocks(index, radius)
        for x in boundary_indexes:
            # check if another animal is on current tile
            for y in self.get_block(x).terrain_animals:
                if(animal.sex != y.sex and animal.species == y.species and y.animal_is_fertile == True):
                    # if species match, sex is compatible spawn new animal 
                    mate_found = True
                    self.move_animal(animal, y.location)
                    self.breed(animal, y, y.location)
                    animal.animal_offspring += 1
                    break
        return mate_found

    # reproduce the given plant (produces clone)
    def reproduce_plant(self, organism, output_location):
        block_index = organism.block_index
        indexes = self.get_neighbor_blocks(block_index) # array of surrounding indexes
        for x in indexes:
            if(self.check_tile_boundary(x)):
                self.log_output("checking potential reproduction site block {}: terrain->{}, occupied->{}".format(x, self.get_block(x).terrain_type, self.get_block(x).terrain_has_plant), output_location) # debug
                if(self.get_block(x).terrain_type == "dirt" and self.get_block(x).terrain_has_plant == False):
                    self.log_output("plant created on block {}: species->{}".format(x, organism.species), output_location) # debug
                    self.env_plants.append(Plant(
                        x, {
                        "species": organism.species,
                        "organism": organism.subspecies,
                        "parent": organism.parent_species,
                        "max_height": self.variate_trait(organism.max_height),
                        "min_moisture": self.variate_trait(organism.min_moisture),
                        "generation": organism.plant_generation + 1,
                        "thorniness": self.variate_trait(organism.plant_thorniness),
                        "excess_water_capacity": self.variate_trait(organism.plant_excess_water_capacity)})
                    )
                    self.get_block(x).terrain_has_plant = True
                    break

    # breed two animals
    def breed(self, a1, a2, location):
        # inherit baseline traits from parents
        species = a1.species
        food_type = a1.food_type
        baby = Animal(location, {
            "species": species,
            "subspecies": a1.subspecies,
            "parent": a1.parent_species,
            "max_size": self.variate_trait((a1.max_size + a2.max_size)/2),
            "min_food": self.variate_trait((a1.min_food + a2.min_food)/2),
            "movement": self.variate_trait((a1.movement + a2.movement)/2),
            "water_movement": self.variate_trait((a1.water_movement + a2.water_movement)/2),
            "food_type": food_type,
            "preferred_terrain": a1.preferred_terrain,
            "wing_size": self.variate_trait((a1.animal_wing_size + a2.animal_wing_size)/2),
            "fin_development": self.variate_trait((a1.animal_fin_development + a2.animal_fin_development)/2),
            "variation_baseline": min(a1.variation_baseline, a2.variation_baseline),
            "generation": a1.animal_generation + 1
        })
        self.get_block(location).terrain_animals.append(baby)
        self.env_animals.append(baby)

   # move animal to random location within radius or known location
    def move_animal(self, animal, new_index=None):
        self.get_block(animal.location).terrain_animals.remove(animal)
        if(new_index == None):
            boundary_indexes = self.get_radial_blocks(animal.location, math.ceil(animal.movement * 3))
            new_index = self.get_random_index({
                            "terrain_type": "dirt",
                            "range": boundary_indexes})
        animal.location = new_index
        distance = abs(animal.location - new_index)
        self.get_block(animal.location).terrain_animals.append(animal)
        animal.animal_food -= distance * 5
        animal.animal_water -= distance * 2

    # simulate the environment
    def simulate(self, days, plants, animals):
        # spawn plants
        for data in plants:
            plant = data.split(",")
            instances = int(plant[4])
            while(instances > 0):
                species = plant[0]
                parent = plant[1]
                max_height = plant[2]
                min_moisture = plant[3]
                self.env_plants.append(Plant(
                    self.get_random_index({
                        "terrain_type": "dirt", 
                        "terrain_has_plant": False}), {
                    "species": species,
                    "parent": parent,
                    "max_height": float(max_height),
                    "min_moisture": float(min_moisture)
                }))
                instances -= 1
        # spawn animals
        for data in animals:
            animal = data.split(",")
            instances = int(animal[6])
            while(instances > 0):
                species = animal[0]
                parent = animal[1]
                max_size = animal[2]
                min_food = animal[3]
                movement = animal[4]
                food_type = animal[5]
                self.env_animals.append(Animal(
                    self.get_random_index({
                        "terrain_type": "dirt", 
                        "terrain_has_plant": False}), {
                    "species": species,
                    "parent": parent,
                    "max_size": float(max_size),
                    "min_food": float(min_food),
                    "movement": float(movement),
                    "food_type": food_type
                }))
                instances -= 1
        # begin simulation
        simulated_days = 0
        while(simulated_days < days):
            output_location = "day{}.txt".format(simulated_days)
            self.log_output("---SIMULATION DAY {}".format(simulated_days), output_location) # debug
            rain_chance = random.randint(0, 100)
            is_raining = False
            if(rain_chance <= self.env_rainfall_frequency):
                is_raining = True
            self.log_output("raining->{}".format(is_raining), output_location)
            # handle block changes
            for x in self.env_tiles:
                x.simulate_daily_background_processes()
                if(is_raining):
                    x.add_rainfall()
            # handle plant processes
            for x in self.env_plants:
                # get corresponding block object for plant
                block = self.get_block(x.block_index)
                # check neighboring blocks for water -> if found, increase moisture level
                boundary_indexes = self.get_neighbor_blocks(x.block_index)
                for index in boundary_indexes:
                    if(self.check_tile_boundary(index)): # make sure block exists
                        if(self.get_block(index).terrain_type == "water"):
                            x.plant_moisture += 1
                # check growth
                x.check_growth(block.terrain_moisture)
                if(simulated_days == 0):
                    # on intial simulation (day 0), tag blocks with plants as occupied
                    block.terrain_has_plant = True
                if(x.plant_health <= 0 and simulated_days > 0):
                    # check if plant needs to be purged (when plant is dead)
                    block.terrain_has_plant = False
                    self.dead_plants.append(x)
                    continue
                if(x.plant_seeds > 0):
                    # convert any uneaten seeds into new organism
                    while(x.plant_seeds > 0): 
                        self.reproduce_plant(x, output_location)
                        x.plant_seeds -= 1
            # handle animal processes
            for x in self.env_animals:
                # check radius for food
                block = self.get_block(x.location)
                self.find_food(x)
                self.find_water(x)
                if(simulated_days == 0):
                    # on intial simulation (day 0), tag blocks with plants as occupied
                    block.terrain_animals.append(x)
                # check growth
                x.check_growth()
                if(x.animal_health <= 0):
                    # check if animal needs to be purged (when animal is dead)
                    self.get_block(x.location).terrain_dead_animals.append(x)
                    self.dead_animals.append(x)
                    continue
                else:
                    mate_found = False
                    if(x.animal_is_fertile):
                        # if animal is fertile, look for suitable mate
                        mate_found = self.find_mate(x)
                    # when finished with daily processes, move the animal if no food/water is found but is needed (expends food + thirst)
                    if((x.animal_food < x.min_food or x.animal_thirst > 0) and mate_found == False):
                        self.move_animal(x)
                # check if animal needs to be saved
                #if(x.animal_saved == False):
                    #if(x.species not in self.animal_species):
                        #self.animal_species[x.species] = {}
            # remove dead plants and animals
            for x in self.dead_plants:
                x.plant_decay_index += 1 # increase decay index
                if x in self.env_plants:
                    # remove living instance from environment if that instance still exists (plant)
                    self.env_plants.remove(x)
                if(x.plant_decay_index >= x.plant_decay_time):
                    # remove dead instance from environment if plant is fully decayed
                    self.dead_plants.remove(x)
            for x in self.dead_animals:
                x.animal_decay_index += 1 # increase decay index
                if x in self.env_animals:
                    # remove living instance from environment if that instance still exists (animal)
                    self.get_block(x.location).terrain_animals.remove(x)
                    self.env_animals.remove(x)
                if(x.animal_decay_index >= x.animal_decay_time):
                    # remove dead instance from environment if animal is fully decayed
                    self.dead_animals.remove(x)
                    self.get_block(x.location).terrain_dead_animals.remove(x)
            self.debug(output_location)
            simulated_days += 1

    # debug function
    def debug(self, output_location):
        # show block data
        coordinate = 0
        terrain_types = {"dirt":0, "water":0}
        for x in self.env_tiles:
            self.log_output("({}) terrain_type->{}, terrain_depth->{}, cluster->{}, moisture->{}".format(coordinate, x.terrain_type, x.terrain_depth, x.cluster_id, x.terrain_moisture), output_location)
            # tally block terrain types
            if(x.terrain_type == "water"):
                terrain_types["water"] += 1
            elif(x.terrain_type == "dirt"):
                terrain_types["dirt"] += 1
            coordinate += 1
        # show plant data
        self.log_output("living plants\n --------------------------------------- ", output_location) # debug
        species = []
        for x in self.env_plants:
            self.log_output(json.dumps(vars(x)), output_location)
            if(x.species not in species):
                species.append(x.species)
        # show collective plant data
        for x in species:
            # show plant count by species
            total = 0
            for y in self.env_plants:
                if x == y.species:
                    total += 1
            self.log_output("{}->{}".format(x, total), output_location) # debug
        # show dead plant data
        self.log_output("dead plants\n --------------------------------------- ", output_location) # debug
        for x in self.dead_plants:
            self.log_output(json.dumps(vars(x)), output_location)
        self.log_output("total living plants->{}".format(len(self.env_plants)), output_location) # debug
        self.log_output("total dead plants->{}".format(len(self.dead_plants)), output_location) # debug
        # show animal data
        self.log_output("living animals\n --------------------------------------- ", output_location) # debug
        species = []
        for x in self.env_animals:
            self.log_output(json.dumps(vars(x)), output_location)
            if(x.species not in species):
                species.append(x.species)
        # show collective animal data
        for x in species:
            # show animal count by species
            total = 0
            for y in self.env_animals:
                if x == y.species:
                    total += 1
            self.log_output("{}->{}".format(x, total), output_location) # debug
        # show dead animal data
        self.log_output("dead animals\n --------------------------------------- ", output_location) # debug
        for x in self.dead_animals:
            self.log_output(json.dumps(vars(x)), output_location)
        self.log_output("total living animals->{}".format(len(self.env_animals)), output_location) # debug
        self.log_output("total dead animals->{}".format(len(self.dead_animals)), output_location) # debug
        






