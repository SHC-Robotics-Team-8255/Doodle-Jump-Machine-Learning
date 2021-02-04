import numpy as np

import random

class Field:

    def __init__(self, row_blocks, col_blocks, block_width, block_height):
        self.row_width = row_blocks
        self.col_height = col_blocks

        self.block_width = block_width
        self.block_height = block_height

        self.field = np.zeros((20, 12), dtype=int)
        self.row_width = 12
        self.col_height = 20
        self.platform_width = 3
        self.platform_needed = True
        self.platform = self.generate_platform()
        self.layers_per_platform = 2
        self.platform_gap=2
        self.layers_left = self.layers_per_platform

        self.total_width = self.block_width * row_width
        self.total_height = self.block_height * self.col_height

        pass  # placeholder

    def update(self):  # main method/function
        #put this all in an if statement of whether or not the player reached the 3rd to the top row?
        self.field = np.delete(self.field, 19, 0)
        if self.platform_gap == 2:
            self.generate_platform()
            self.platform_gap-=1
        else:
            self.field = np.insert(self.field, 0, np.zeros(self.row_width), 0)
        if self.coin_random:
            self.generate_coin()
        if self.platform_gap==0:
            self.platform_gap = 2
        
    def coin_random(self):
        #randomizer code here
        return False

    def generate_coin(self):
        pass

    def generate_platform(self):
        platform = np.rows(self.row_width)
        platform_start = random.randrange(0, self.row_width-self.platform_width)
        for i in range(platform_start, platform_start + self.platform_width):
            platform[i] = 3

        return platform

    def copy(self):
        return self.field.copy()


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.field.__repr__()

    def color(self, n):
        if np.equal(n, 0):
            return (0, 0, 0)
        if np.equal(n, 3):
            return (255, 255, 255)
        if np.equal(n, 4):
            return (0, 255, 255)
        return (255, 0, 0)
        #at least i think this is red


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 field.py. Use this for testing")
    field = Field()
    field.update()
    print(field.field)
