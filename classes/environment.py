class Environment:

    # environment conditions
    env_size = 0
    env_water_percentage = 0
    env_water_distribution = 0
    env_rainfall_frequency = 0
    
    # environment content
    env_arr = None

    # generate environment base
    def __init__(self, size, water_percentage, water_distribution, rainfall_frequency):

        # create 2d array
        rows, cols = (size, size)
        arr = [[None]*cols]*rows

        # reassign variables
        self.env_size = size
        self.env_water_percentage = water_percentage
        self.env_water_distribution = water_distribution
        self.env_rainfall_frequency = rainfall_frequency

