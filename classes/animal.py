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
        self.min_food = args["min_food"] # minimum food required per turn
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
        # dynamic properties
        self.animal_water = 0
        self.animal_food = 0
        self.animal_health_max = 100
        self.animal_health = self.animal_health_max
        self.animal_age = 0
        self.animal_size = 1.0
        self.animal_offspring = 0
        self.animal_is_fertile = False

    # handle growth of the animal
    def check_growth(self, food):
        self.animal_food += food
        if(self.animal_food >= self.min_food):
            self.grow(food)
        if(self.animal_health > 0):
            # if animal health is greater than zero, age the animal
            self.animal_age += 1
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
    def grow(self, food):
        # automatically grow and heal animal
        self.animal_size += self.growth_rate
        self.animal_health += 10
        if(self.animal_size > self.max_size):
            # ensure size doesn't exceed maximum
            self.animal_size = self.max_size
        if(self.animal_health > self.animal_health_max):
            # ensure animal health doesn't exceed maximum
            self.animal_health = self.animal_health_max
