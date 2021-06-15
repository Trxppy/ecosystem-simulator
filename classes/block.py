# import modules

class Block:
    # individual block units in environment

    # block properties
    terrain_generated = False
    terrain_type = None
    terrain_feature = None
    terrain_group = None
    terrain_depth = 0
    
    def __init__(self):
        # initialize block
        self.terrain_type = "dirt"
        self.terrain_depth = 3

    def set_terrain(self, type, depth):
        # set terrain properties
        self.terrain_type = type
        self.terrain_depth = depth
        self.terrain_generated = True
    def reset_terrain(self):
        # reset block to default state
        self.terrain_type = "dirt"
        self.terrain_depth = 3
        self.terrain_generated = False
        self.terrain_group = None

