# import modules
import math
import random


class Animal:
    # animal entity

    def __init__(self, block_index, args):
        # static (user-defined) properties
        self.block_index = block_index
        self.species = args["species"]