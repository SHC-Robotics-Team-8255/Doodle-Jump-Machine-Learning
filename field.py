import numpy as np


class Field:

    def __init__(self):
        self.field = np.zeros(1, dtype=int)
        pass  # placeholder

    def update(self):  # main method/function
        pass

    def generate_coin(self):
        pass

    def generate_platform(self):
        pass

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
