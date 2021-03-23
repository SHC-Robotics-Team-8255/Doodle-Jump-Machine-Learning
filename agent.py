from game import Game
import os

import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import imageio

from tf_agents.environments import utils
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import tf_py_environment
from tf_agents.utils import common
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.policies import policy_saver

import cv2
# os.mkdir(os.path.join(os.getcwd(), "artifacts"))
# with open("artifacts/artifact.txt", "w") as file:
#    file.write("test123")

try:
    os.mkdir(os.path.join(os.getcwd(), "artifacts"))
except FileExistsError:
    pass

def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():  # game over
            action_step = policy.action(time_step)  # generate a decision -> 0,1
            time_step = environment.step(action_step.action) # decision acts on env
            # cv2.imshow('frame', cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
            # cv2.waitKey(100)
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

    num_iterations = 100000  # @param {type:"integer"}

    initial_collect_steps = 200  # @param {type:"integer"}
    collect_steps_per_iteration = 1  # @param {type:"integer"}
    replay_buffer_max_length = 100000  # @param {type:"integer"}

    batch_size = 64  # @param {type:"integer"}
    learning_rate = 1e-3  # @param {type:"number"}
    # learning_rate = tf.keras.optimizers.schedules.InverseTimeDecay(1e-4, decay_steps=1000, decay_rate=1)
    log_interval = 2000  # @param {type:"integer"}

    num_eval_episodes = 20  # @param {type:"integer"}
    eval_interval = 5000  # @param {type:"integer"}

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

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=train_env.batch_size,
        max_length=replay_buffer_max_length)

    def collect_step(environment, policy, buffer):
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step, next_time_step)

        # Add trajectory to the replay buffer
        buffer.add_batch(traj)


    def collect_data(env, policy, buffer, steps):
        for _ in range(steps):
            collect_step(env, policy, buffer)

    collect_data(train_env, random_policy, replay_buffer, initial_collect_steps)

    dataset = replay_buffer.as_dataset(
        num_parallel_calls=3,
        sample_batch_size=batch_size,
        num_steps=2).prefetch(3)

    iterator = iter(dataset)

    agent.train = common.function(agent.train)

    # Reset the train step
    agent.train_step_counter.assign(0)

    avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
    returns = [avg_return]

    tf_policy_saver = policy_saver.PolicySaver(agent.policy)

    for _ in range(num_iterations):
        collect_data(train_env, agent.collect_policy, replay_buffer, collect_steps_per_iteration)

        experience, unused_info = next(iterator)
        train_loss = agent.train(experience).loss # loss=change

        step = agent.train_step_counter.numpy()

        if step % log_interval == 0:
            print('step = {0}: loss = {1}'.format(step, train_loss))

        if step % eval_interval == 0:
            avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
            print('step = {0}: Average Return = {1}'.format(step, avg_return))
            returns.append(avg_return)
            policy_dir = os.path.join(os.getcwd(),
                                      f'policies/epoch_run/policy_{round(step)}')
            tf_policy_saver.save(policy_dir)


    def create_policy_eval_video(policy, filename, num_episodes=20, fps=12):
        with imageio.get_writer(filename, fps=fps) as video:
            for _ in range(num_episodes):
                time_step = eval_env.reset()
                video.append_data(cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
                while not time_step.is_last():
                    action_step = policy.action(time_step)
                    time_step = eval_env.step(action_step.action)
                    video.append_data(cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))

                    # cv2.imshow('frame', cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
                    # cv2.waitKey(13)


    print(compute_avg_return(eval_env, random_policy, num_eval_episodes))

    iterations = range(0, num_iterations + 1, eval_interval)
    plt.plot(iterations, returns)
    plt.ylabel('Average Return')
    plt.xlabel('Iterations')
    # plt.show()

    create_policy_eval_video(agent.policy, "artifacts/test.mp4")

    create_policy_eval_video(agent.policy, "artifacts/test.mp4")

    print("done")
