# import modules

class Block:
    # individual block entity

    # block properties
    terrain_generated = False
    terrain_type = None
    terrain_feature = None
    terrain_group = None
    terrain_depth = 0
    
    def __init__(self, index):
        # initialize block
        self.terrain_type = "dirt"
        self.terrain_depth = 3
        self.terrain_moisture = 0
        self.cluster_id = None
        self.index = index
        self.terrain_has_plant = False
        self.terrain_animals = []
        self.terrain_water_depth = 0

    def set_terrain(self, type, depth):
        # set terrain properties
        self.terrain_type = type
        self.terrain_depth = depth
        self.terrain_generated = True

    def set_water_depth(self, depth):
        self.terrain_water_depth = depth

    def set_cluster(self, type, id):
        # set cluster group
        self.cluster_type = type
        self.cluster_id = id

    def add_rainfall(self):
        # add rainfall effects to block
        self.terrain_moisture += 0.2

    def simulate_daily_background_processes(self):
        # simulate background processes at the start of a new day
        if(self.terrain_moisture > 0):
            # dry terrain
            self.terrain_moisture -= 0.1 # dry

    def reset_terrain(self):
        # reset block to default state
        self.terrain_type = "dirt"
        self.terrain_depth = 3
        self.terrain_generated = False
        self.terrain_group = None

