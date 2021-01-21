import numpy as np
import cv2

from field import Field


class Game:
    def __init__(self):
        self.x = 7
        self.y = 7
        self.is_going_up = True
        self.bump_platform = False
        self.base_field = Field()
        self.active_field = self.base_field.copy()
        self.active_field = np.zeros((12,20))
        pass

    def _step(self, action):
        print(action)  # main function

    def render(self):
        cv2.imshow('game', cv2.resize(self.active_field, (240, 400), interpolation=cv2.INTER_NEAREST))


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 game.py. Use this for testing")
    game = Game()

    num_frames_to_test = 10
    for i in range(num_frames_to_test):

        cv2.imshow('game', np.zeros((400, 240)))

        key = cv2.waitKey(0)
        go_right = False
        valid_key = False

        while not valid_key:
            if key == ord('a'):
                go_right = False
                valid_key = True
            elif key == ord('d'):
                go_right = True
                valid_key = True

        game._step(int(go_right))
        game.render()

        self.active_field[6][7] = 3
        self.active_field[6][8] = 3
        self.active_field[6][9] = 3

        self.active_field[self.x][self.y] = 2

        if is_going_up == True 
            for i in range(12):
                x += 1
            is_going_up = False
        if is_going_up == False
            if bump_platfom == True 
                is_going_up = True
            else
                x -= 1
        
        if is_going_up == False and 5 in active_field:
            bump_platform = True

