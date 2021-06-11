class Environment:

    # environment conditions
    env_size = 0
    env_water_percentage = 0
    env_rainfall_frequency = 0
    
    # environment content
    env_arr = None

    # generate environment
    def __init__(self, size, water_percentage, rainfall_frequency):

        # create 2d array
        rows, cols = (size, size)
        arr = [[0]*cols]*rows
        print(arr)

        # reassign variables
        self.env_size = size
        self.env_water_percentage = water_percentage
        self.env_rainfall_frequency = rainfall_frequency

