from game import Game
import os

import tensorflow as tf

from tf_agents.environments import utils
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import tf_py_environment
from tf_agents.utils import common
from tf_agents.policies import random_tf_policy
import cv2
# os.mkdir(os.path.join(os.getcwd(), "artifacts"))
# with open("artifacts/artifact.txt", "w") as file:
#    file.write("test123")


def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():  # game over
            action_step = policy.action(time_step)  # generate a decision -> 0,1
            time_step = environment.step(action_step.action) # decision acts on env
            cv2.imshow('frame', cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(100)
            episode_return += time_step.reward
        total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]

if __name__ == "__main__":
    
    environment = Game()
    utils.validate_py_environment(environment, episodes=5)

    train_env = tf_py_environment.TFPyEnvironment(Game())
    eval_env = tf_py_environment.TFPyEnvironment(Game())

    fc_layer_params = (20, 12)

    learning_rate = 1e-4

    q_net = q_network.QNetwork(
        train_env.observation_spec(),
        train_env.action_spec(),
        fc_layer_params=fc_layer_params)

    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

    train_step_counter = tf.Variable(0)

    random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                    train_env.action_spec())

    agent = dqn_agent.DqnAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)


    print(compute_avg_return(eval_env, random_policy))

    print("done")