import numpy as np
import random

class Field:

    def __init__(self):
        self.field = np.zeros(1, dtype=int)
        self.row_width = 12
        self.platform_width = 3
        self.platform_needed = True
        # placeholder

    def update(self):  # main method/function
        if self.platform_needed:
            self.generate_platform()
            self.platform_needed = False
        

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


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 field.py. Use this for testing")
    field = Field()
    field.update()
    print(field.field)
