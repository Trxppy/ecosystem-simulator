# import modules
import math
import random


class Plant:
    # plant entity -> any organism fixed to one block + receives energy from sun + water

    def __init__(self, block_index, args):
        # initialize plant
        # static (user-defined) properties
        self.block_index = block_index
        self.species = args["species"]
        self.max_height = args["max_height"]
        self.min_moisture = args["min_moisture"] # per turn
        # static calculated properties
        self.growth_rate = (self.max_height/self.min_moisture)/100
        self.lifespan = (self.max_height/self.growth_rate) * 2 # double the time it takes to reach full height
        self.lifespan = random.randint(math.floor(self.lifespan * .9), math.ceil(self.lifespan * 1.1)) # add variability to lifespan
        self.seed_rate = self.lifespan/5 # rate at which seeds are added
        # dynamic properties
        self.plant_seeds = 0
        self.plant_height = 0
        self.plant_moisture = 0
        self.plant_excess_water = 0
        self.plant_health = 100
        self.plant_age = 0

    def check_growth(self, moisture):
        # add moisture to the plant and calculate the subsequent growth
        self.plant_moisture += moisture
        if(self.plant_moisture > self.min_moisture):
            # if excess moisture detected, store as excess water (can be consumed by other organisms or the plant in case of drought)
            self.plant_excess_water = self.plant_moisture - self.min_moisture
            self.plant_moisture = self.min_moisture
            self.grow()
        elif(self.min_moisture > self.plant_moisture):
            # if minimum moisture not met, check excess reserves
            if(self.plant_excess_water >= self.min_moisture):
                # if enough excess water is found, continue growth
                self.plant_moisture = self.plant_excess_water - self.min_moisture    
                self.plant_excess_water = self.plant_excess_water - self.min_moisture
                self.grow()
            else:          
                # if not enough excess water is found, take damage
                self.plant_moisture = self.plant_excess_water
                self.plant_excess_water = 0   
                self.plant_health -= 5
        else:
            # if plant has just enough moisture, set excess to zero
            self.plant_excess_water = 0
            self.plant_moisture = self.min_moisture
        # ensure health doesn't fall below zero
        if(self.plant_health <= 0):
            # set plant health to zero (plant will die)
            self.plant_health = 0
        if(self.plant_health > 0):
            # if plant health is greater than zero, age the plant
            self.plant_age += 1
            if(self.plant_age >= self.lifespan):
                # if plant has reached the end of its lifespan, set health to zero
                self.plant_health = 0
            elif(self.plant_height == self.max_height and self.plant_health == 100):
                # if plant is at maximum health and height, add seeds
                self.plant_seeds += self.seed_rate

    # grow current plant at default growth rate
    def grow(self):
        # ensure height doesn't exceed maximum
        self.plant_height += self.growth_rate
        self.plant_health += 10
        if(self.plant_height > self.max_height):
            self.plant_height = self.max_height
        if(self.plant_health > 100):
            self.plant_health = 100
