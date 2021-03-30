import numpy as np
import cv2

from field import Field

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec, tensor_spec
from tf_agents.trajectories import time_step as ts

class Game(py_environment.PyEnvironment):
    def __init__(self, limit=True):

        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=1, name="action"
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(20, 12), dtype=np.int32, minimum=0, name="observation"
        )

        self.x = 6
        self.y = 2
        self.is_going_up = False
        self.bump_platform = False
        self.base_field = Field()
        self.active_field = self.base_field.copy()
        self.reward = 0
        self.up_frame_left = 7

        self.frames = 0
        self._step_count = 0
        self._episode_ended = False
        self.limit = limit

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._step_count = 0
        self.frames = 0
        self.is_going_up = False
        self.up_frame_left = 7
        self.x = 6
        self.y = 2
        self.field = Field()
        self._episode_ended = False
        self.active_field = self.field.copy()
        self.active_field[self.y][self.x] += 2
        self.reward = 0
        return ts.restart(self.active_field)

    def _step(self, action):
        # print(action)  # main function

        self.reward = 1  # 1 3/10

        if self.limit and self._step_count > 10000:
            self._episode_ended = True
            reward = 100
            return ts.termination(self.active_field, reward)

        if self._episode_ended:
            return self.reset()

        self.frames += 1
        self._step_count += 1
        while self.frames <= 13:
            self.base_field.update()
            self.frames += 1

        self.moving_sideways(action)
        self.jump()

        self.base_field.update()
        self.active_field = self.base_field.copy()

        self.active_field[self.y][self.x] += 2

        if self.y <= 1:
            self.is_going_up = False
            # self.reward += 10

        if self.y >= 17:
            self._episode_ended = True
            return ts.termination(self.active_field, -100)
            print("Game Over")
        
        return ts.transition(self.active_field, self.reward, 1)

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
          
    def render(self, *args):

        render = np.zeros((20, 12, 3))

        for row in range(len(self.active_field)):
            for block in range(len(self.active_field[row])):
                render[row][block] = list(self.create_color(self.active_field[row][block]))
                
        return render

    def jump(self):

        if 3 in self.active_field:
            self.is_going_up = True
            self.up_frame_left = 7
            # self.reward += 15 7/10

        #if 6 in self.active_field:
        #    self.reward += 5
    
        if self.is_going_up:
            # self.reward += 2
            self.y -= 1
            self.up_frame_left -= 1
            if self.up_frame_left == 0:
                self.is_going_up = False
        else:
            self.y += 2

    def moving_sideways(self,action):
        if action == 1:
            self.x = min(11, self.x + 1)  # if x < 11: x += 1
        if action == 0:
            self.x = max(0, self.x - 1)
            """
            -2 | 0
            -1 | 0
            0 | 0
            1 | 0
            2 | 1
            """


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
