from game import Game
import os

os.mkdir(os.path.join(os.getcwd(), "artifacts"))
with open("artifacts/artifact.txt", "w") as file:
    file.write("test123")
