import agent
import tensorflow as tf
import cv2
from tf_agents.environments import tf_py_environment
import imageio

eval_env = tf_py_environment.TFPyEnvironment(agent.Game(limit=False))


def create_policy_eval_video(policy, filename, num_episodes=20, fps=12):
    with imageio.get_writer(filename, fps=fps) as video:
        for _ in range(num_episodes):
            time_step = eval_env.reset()
            video.append_data(cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
            while not time_step.is_last():
                action_step = policy.action(time_step)
                time_step = eval_env.step(action_step.action)
                video.append_data(cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
                cv2.imshow('frame',
                           cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
                cv2.waitKey(13)



saved_policy = tf.compat.v2.saved_model.load('policies/epoch_run/policy_90000')
time_step = eval_env.reset()
#create_policy_eval_video(saved_policy, "final.mp4",  num_episodes=5, fps=12)
#exit()
while True:
    policy_step = saved_policy.action(time_step)
    time_step = eval_env.step(policy_step.action)
    cv2.imshow('frame', cv2.resize(eval_env.render()[0].numpy(), (240, 400), interpolation=cv2.INTER_NEAREST))
    cv2.waitKey(33)
    if time_step.is_last():
        time_step = eval_env.reset()
