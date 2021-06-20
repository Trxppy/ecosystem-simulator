# import modules
import math
import random


class Animal:
    # animal entity

    def __init__(self, block_index, args):
        # static (user-defined) properties
        self.block_index = block_index
        self.species = args["species"]
        self.max_size = args["max_size"] # x% of 100, with size of 100 representing one block
        self.min_food = args["min_food"] # minimum food required per turn
        # static calculated properties
        self.growth_rate = (self.max_size/self.min_food)
        self.lifespan = (self.max_size/self.growth_rate) * 2 # double the time it takes to reach full size
        self.lifespan = random.randint(math.floor(self.lifespan * .9), math.ceil(self.lifespan * 1.1)) # add variability to 
        # dynamic properties
        self.animal_thirst = 0
        self.animal_hunger = 0
        self.animal_health = 100
        self.animal_age = 0
        self.animal_size = 0