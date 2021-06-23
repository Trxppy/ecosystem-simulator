# import modules
import math
import random
import os, shutil
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
        # reassign variables
        self.env_size = size * size
        self.env_width = size
        self.env_water_percentage = water_percentage
        self.env_water_distribution = water_distribution
        self.env_rainfall_frequency = rainfall_frequency
        # generation variables
        self.env_water_clusters = 0
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
                current_tile.set_terrain("water", random.randint(3, 5))
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
        f = open('output/' + location, "a")
        f.write(line + "\n")
        f.close()

    # delete contents of output folder
    def clear_output(self):
        folder = 'output/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            os.unlink(file_path)

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

    # return block given index
    def get_block(self, index):
        for x in self.env_tiles:
            if(x.index == index):
                return x
        return None

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

    # retrieve index from random block
    def get_random_index(self):
        index = random.randint(0, self.env_size-1)
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
        radial_blocks = []
        radius = int(radius)
        while(radius > 0):
            if(self.check_tile_boundary(index + radius)):
                # east block
                radial_blocks.append(index + radius)
            if(self.check_tile_boundary(index - radius)):
                # west block
                radial_blocks.append(index - radius)
            if(self.check_tile_boundary(index + (self.env_width * radius))):
                # north block
                radial_blocks.append(index + (self.env_width * radius))
            if(self.check_tile_boundary(index - (self.env_width * radius))):
                # south block
                radial_blocks.append(index - (self.env_width * radius))
            if(self.check_tile_boundary(index - (self.env_width * radius) + radius)):
                # northeast block
                radial_blocks.append(index + (self.env_width * radius) + radius)
            if(self.check_tile_boundary(index + (self.env_width * radius) - radius)):
                # northwest block
                radial_blocks.append(index + (self.env_width * radius) - radius)
            if(self.check_tile_boundary(index - (self.env_width * radius) + radius)):
                # southeast block
                radial_blocks.append(index - (self.env_width * radius) + radius)
            if(self.check_tile_boundary(index - (self.env_width * radius) - radius)):
                # southwest block
                radial_blocks.append(index - (self.env_width * radius) - radius)
            radius -= 1
        return radial_blocks

    # retrieve index from random block with terrain parameter
    def get_random_index(self, terrain_type, is_occupied):
        valid = False
        index = 0
        failsafe_index = 1000 # attempts before breaking loop
        while(valid == False):
            index = random.randint(0, self.env_size-1)
            if(self.get_block(index).terrain_type == terrain_type and self.get_block(index).terrain_occupied == is_occupied):
                valid = True
            if(index == failsafe_index):
                break
        return index

    # find food location
    def find_food(self, index, movement, food_type):
        food = 0
        radius = movement * 3
        boundary_indexes = self.get_radial_blocks(index, radius)
        for x in boundary_indexes:
            if(food_type == "herbivore"):
                # if herbivore, check if block has plant
                if(self.get_plant(x) != False):
                    # if plant found, check if plant has enough health to be eaten
                    if(self.get_plant(x).plant_health > 0):
                        food += 1
                        self.get_plant(x).plant_health -= 1
        return food

    # simulate the environment
    def simulate(self, days, plants, animals):
        # spawn plants
        for data in plants:
            plant = data.split(",")
            instances = int(plant[3])
            while(instances > 0):
                species = plant[0]
                max_height = plant[1]
                min_moisture = plant[2]
                self.env_plants.append(Plant(
                    self.get_random_index("dirt", False), {
                    "species": species,
                    "max_height": float(max_height),
                    "min_moisture": float(min_moisture)
                }))
                instances -= 1
        # spawn animals
        for data in animals:
            animal = data.split(",")
            instances = int(animal[5])
            while(instances > 0):
                species = animal[0]
                max_size = animal[1]
                min_food = animal[2]
                movement = animal[3]
                food_type = animal[4]
                self.env_animals.append(Animal(
                    self.get_random_index("dirt", False), {
                    "species": species,
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
                    block.terrain_occupied = True
                if(x.plant_health == 0):
                    # check if plant needs to be purged (when plant is dead)
                    block.terrain_occupied = False
                    self.env_plants.remove(x)
                if(x.plant_seeds > 0):
                    # convert any uneaten seeds into new organism
                    while(x.plant_seeds > 0): 
                        self.reproduce_plant(x, output_location)
                        x.plant_seeds -= 1
            # handle animal processes
            for x in self.env_animals:
                # check radius for food
                food_found = self.find_food(x.location, x.movement, x.food_type)
                # check growth
                x.check_growth(food_found)
                if(x.animal_health == 0):
                    # check if animal needs to be purged (when animal is dead)
                    self.env_animals.remove(x)
            self.debug(output_location)
            simulated_days += 1

    # reproduce the given plant (produces clone)
    def reproduce_plant(self, organism, output_location):
        block_index = organism.block_index
        indexes = self.get_neighbor_blocks(block_index) # array of surrounding indexes
        for x in indexes:
            if(self.check_tile_boundary(x)):
                self.log_output("checking potential reproduction site block {}: terrain->{}, occupied->{}".format(x, self.get_block(x).terrain_type, self.get_block(x).terrain_occupied), output_location) # debug
                if(self.get_block(x).terrain_type == "dirt" and self.get_block(x).terrain_occupied == False):
                    self.log_output("plant created on block {}: species->{}".format(x, organism.species), output_location) # debug
                    self.env_plants.append(Plant(
                        x, {
                        "species": organism.species,
                        "max_height": organism.max_height,
                        "min_moisture": organism.min_moisture}))
                    self.get_block(x).terrain_occupied = True
                    break

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
        species = []
        for x in self.env_plants:
            self.log_output("({}) species->{}, moisture->{}, excess->{}, height->{}, health->{}, age->{}, estimated lifespan->{}".format(x.block_index, x.species, x.plant_moisture, x.plant_excess_water, x.plant_height, x.plant_health, x.plant_age, x.lifespan), output_location)
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
        self.log_output("total plants->{}".format(len(self.env_plants)), output_location) # debug
        # show animal data
        species = []
        for x in self.env_animals:
            self.log_output("({}) species->{}, max_size->{}, current_size->{}, health->{}, age->{}, estimated lifespan->{}, food->{}, water->{}".format(x.location, x.species, x.max_size, x.animal_size, x.animal_health, x.animal_age, x.lifespan, x.animal_food, x.animal_water), output_location)
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
        self.log_output("total animals->{}".format(len(self.env_animals)), output_location) # debug
        






