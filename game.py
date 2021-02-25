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
        self.up_frame_left = 7

    def _step(self, action):
        print(action)  # main function

        if self.y >= 19:
            return False
            print("Game Over")
        else:
            #print(self.reward + 1)
            self.base_field.update()
            self.active_field = self.base_field.copy()
            self.moving_sideways(action)
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
        else: # 5
            return (0, 255, 0)
          
    def render(self):

        render = np.zeros((20, 12, 3))

        for row in range(len(self.active_field)):
            for block in range(len(self.active_field[row])):
                render[row][block] = list(self.create_color(self.active_field[row][block]))
                
        return render

    def jump(self):
  
        self.active_field[self.y][self.x] += 2
        
        if self.is_going_up == False and 5 in self.active_field:
            self.is_going_up = True
            self.up_frame_left = 7
    
        if self.is_going_up:
            self.y -= 1
            self.up_frame_left -= 1
            if self.up_frame_left == 0:
                self.is_going_up = False
        else:
            self.y += 2

    def moving_sideways(self,action):
        if action == 1:
            self.x +=1
        if action == 0:
            self.x -=1


if __name__ == "__main__":
    print("This code will only be executed when this is the file being called, "
          "like python/python3 game.py. Use this for testing")
    game = Game()

    num_frames_to_test = 100
    for i in range(num_frames_to_test):

        cv2.imshow('game', cv2.resize(game.render(), (240, 400), interpolation=cv2.INTER_NEAREST))

        go_right = False
        valid_key = False

        while not valid_key:
            key = cv2.waitKey(0)
            if key == ord('a'):
                go_right = False
                valid_key = True
            elif key == ord('d'):
                go_right = True
                valid_key = True

        if not game._step(int(go_right)):
            break
