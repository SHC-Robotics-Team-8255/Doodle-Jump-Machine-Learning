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
        self.reward = 0

    def _step(self, action):
        print(action)  # main function

        if self.y >= 19:
            return False
            print("Game Over")
        else:
            print(self.reward + 1)
            self.base_field.update()
            self.active_field = self.base_field.copy()
            self.jump()
            self.reward = 0
            return True

    def create_color(self, number):
        if np.equal(number, 0):
            return (255, 255, 255)
        elif np.equal(number, 2):
            return (255, 0, 0)
        elif np.equal(number, 3):
            return (0, 0, 0)
        elif np.equal(number, 4):
            return (0, 255, 255)
        else: 
            self.y = True
            return print(self.y)
          
    def render(self):

        render = np.zeros((20, 12, 3))

        for row in range(len(self.active_field)):
            for block in range(len(self.active_field[row])):
                render[row][block] = list(self.create_color(self.active_field[row][block]))
                
        return render

    def jump(self):
  
        self.active_field[self.x][self.y] = 2
    
        if self.is_going_up:
            for i in range(12):
                self.x -= 1
            self.is_going_up = False
        else:
            if self.bump_platform == True: 
                self.is_going_up = True
            else:
                self.x += 1
        
        if self.is_going_up == False and 5 in self.active_field:
            self.bump_platform = True


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 game.py. Use this for testing")
    game = Game()

    num_frames_to_test = 10
    for i in range(num_frames_to_test):

        cv2.imshow('game', cv2.resize(game.render(), (240, 400), interpolation=cv2.INTER_NEAREST))

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

        if game._step(int(go_right)):
            break
        
  
