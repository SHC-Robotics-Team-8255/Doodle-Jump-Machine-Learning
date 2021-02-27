from game import Game
import os

os.mkdir(os.path.join(os.getcwd(), "artifacts"))
with open("artifacts/artifact.txt") as file:
    file.write("test123")
