# import modules
import math
import random


class Animal:
    # animal entity

    def __init__(self, block_index, args):
        # static (user-defined) properties
        self.location = block_index
        self.species = args["species"]
        self.max_size = args["max_size"] # x% of 100, with size of 100 representing one block
        self.min_food = args["min_food"] + (args["max_size"]/50) # minimum food required per turn
        self.movement = args["movement"]
        self.food_type = args["food_type"]
        # static calculated properties
        self.growth_rate = (self.max_size/self.min_food)
        self.sex = random.choice(['male','female'])
        self.lifespan = (self.max_size/self.growth_rate) * 2 # double the time it takes to reach full size
        self.lifespan = random.randint(math.floor(self.lifespan * .9), math.ceil(self.lifespan * 1.1)) # add variability
        if(self.lifespan == 0):
            # ensure lifespan is at least 1
            self.lifespan = 1
        self.maturity_age = math.ceil(self.lifespan * .7)
        self.offspring_max = math.ceil(self.lifespan/4)
        self.min_water = math.ceil(self.min_food/3)
        # dynamic properties
        self.animal_generation = 1
        if "generation" in args:
            # override default generation var if passed as parameter
            self.animal_generation = args["generation"]
        self.animal_water = 0
        self.animal_thirst = 0
        self.animal_food = 0
        self.animal_health_max = 100
        self.animal_health = self.animal_health_max
        self.animal_age = 0
        self.animal_size = 1.0
        self.animal_offspring = 0
        self.animal_is_fertile = False
        self.animal_stomach = []
        self.animal_acquired_taste = None
        self.animal_wing_size = 1
        if "wing_size" in args:
            # override default generation var if passed as parameter
            self.animal_wing_size = args["wing_size"]
            if(self.animal_wing_size >= 5):
                self.movement *= 1.2
            if(self.animal_wing_size >= 25):
                self.movement *= 1.5

    # handle growth of the animal
    def check_growth(self):
        self.animal_age += 1 # age the animal
        self.analyze_stomach() # analyze stomach contents
        if(self.animal_food >= self.min_food and self.animal_thirst <= 0):
            # grow animal if sufficient food and water detected
            self.animal_thirst = 0 
            self.grow()
        elif(self.animal_thirst > 0):
            # otherwise, if insufficent water detected, subtract health
            self.animal_health -= 20
        if(self.animal_health > 0):
            if(self.animal_age >= self.lifespan):
                # if animal has reached the end of its lifespan, set health to zero
                self.animal_health = 0
            elif(self.animal_food < self.min_food):
                # if animal doesn't have enough food, subtract health points
                self.animal_health -= 10
                if(self.animal_food < 0):
                    # if animal has negative food, set food to zero
                    self.animal_food = 0
            elif(self.animal_size == self.max_size and self.animal_health == self.animal_health_max and self.animal_age >= self.maturity_age):
                # if animal is at maximum health and size, has reached maturity, and has not reached max offspring, mark animal as fertile
                if(self.animal_offspring < self.offspring_max):
                    # only mark animal as fertile if max offspring isn't reached
                    self.animal_is_fertile = True
                else:
                    self.animal_is_fertile = False

    # grow organism
    def grow(self):
        # automatically grow and heal animal
        self.animal_size += self.growth_rate
        self.animal_size = round(self.animal_size, 2) # round animal size
        self.animal_health += 10
        if(self.animal_size > self.max_size):
            # ensure size doesn't exceed maximum
            self.animal_size = self.max_size
        if(self.animal_health > self.animal_health_max):
            # ensure animal health doesn't exceed maximum
            self.animal_health = self.animal_health_max

    # analyze stomach for acquired taste
    def analyze_stomach(self):
        counter = 0
        num = None
        list = self.animal_stomach
        if(len(self.animal_stomach) > 5):
            # if stomach has sufficient content, find most frequent item
            for i in list:
                frequency = list.count(i)
                if(frequency > counter):
                    counter = frequency
                    num = i
            self.animal_acquired_taste = num
