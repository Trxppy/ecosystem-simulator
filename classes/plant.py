# import modules

class Plant:
    # plant entities

    def __init__(self, block_index, args):
        # initialize plant
        # static (user-defined) properties
        self.block = block_index
        self.name = args["name"]
        self.max_height = args["max_height"]
        self.min_moisture = args["min_moisture"] # per turn
        # static calculated properties
        self.growth_rate = (self.max_height/self.min_moisture)/50
        # dynamic properties
        self.plant_height = 0
        self.plant_moisture = 0
        self.plant_excess_water = 0
        self.plant_health = 100

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
        if(self.plant_health < 0):
            self.plant_health = 0

    # grow current plant at default growth rate
    def grow(self):
        # ensure height doesn't exceed maximum
        self.plant_height += self.growth_rate
        if(self.plant_height > self.max_height):
            self.plant_height = self.max_height