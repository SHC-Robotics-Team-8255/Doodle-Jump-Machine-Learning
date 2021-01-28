import numpy as np

import random

class Field:

    def __init__(self, row_blocks, col_blocks, block_width, block_height):
        self.row_width = row_blocks
        self.col_height = col_blocks

        self.block_width = block_width
        self.block_height = block_height

        self.field = np.zeros(1, dtype=int)
        self.row_width = 12
        self.col_height = 20
        self.platform_width = 3
        self.platform_needed = True
        self.platform = self.generate_platform()
        self.layers_per_platform = 2
        self.layers_left = self.layers_per_platform

        self.total_width = self.block_width * row_width
        self.total_height = self.block_height * self.col_height

        pass  # placeholder

    def update(self):  # main method/function
        if self.platform_needed:
            generate_platform(self)
            self.platform_needed = False
        return_true = False 
        if self.field[12][0] == 1 and not self.platform_needed:
            self.platform_needed = True
            self.platform = self.generate_platform()
            return_true = True

        self.field = np.delete(self.field, 12, 0)
        if self.platform_needed:
            self.field = np.insert(self.field, 0, self.platform,0)
            self.layers_left -= 1
            if self.layers_left == 0:
                self.platform_needed = False
                self.layers_left = self.layers_per_platform
        else:
            self.field = np.insert(self.field, 0, np.zeros(self.row_width, int), 0)

        return return_true

    def generate_coin(self):
        pass

    def generate_platform(self):
        pass
        platform = np.rows(self.row_width)
        platform_start = random.randrange(0, self.row_width-self.platform_width)
        for i in range(platform_start, platform_start + self.platform_width):
            platform[i] = 3

        return platform

    def copy(self):
        return self.field.copy()


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 field.py. Use this for testing")
    field = Field()
    field.update()
    print(field.field)
