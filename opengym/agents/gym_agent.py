import argparse
import sys
import numpy as np
import gym
from gym import wrappers, logger

class QLearning(object):
    def __init__(self,myenv):
        self.env = gym.make(myenv)
        self.MAXSTATES = 10 ** 4
        self.GAMMA = 0.9
        self.ALPHA = 0.01

    def max_dict(self,d):
        max_v = float("-inf")
        for key, val in d.items():
            if val > max_v:
                max_v = val
                max_key = key
        return max_key, max_v

    def create_bins(self):

        bins = np.zeros([4, 10])
        bins[0] = np.linspace(-4.8, 4.8, 10)
        bins[1] = np.linspace(-5, 5, 10)
        bins[2] = np.linspace(-.418, .418, 10)
        bins[3] = np.linspace(-5, 5, 10)

        return bins

    def assign_bins(self,observation, bins):
        state = np.zeros(4)
        for i in range(4):
            state[i] = np.digitize(observation[i], bins[i])
        return state

    def get_state_as_string(self,state):
        string_state = ''.join(str(int(e)) for e in state)
        return string_state

    def get_all_states_as_string(self):
        states = []
        for i in range(self.MAXSTATES):
            states.append(str(i).zfill(4))
        return states

    def initialize_Q(self):
        Q = {}

        all_states = self.get_all_states_as_string()
        for state in all_states:
            Q[state] = {}
            for action in range(self.env.action_space.n):
                Q[state][action] = 0

        return Q

    def Q_act(self, Q, observation, eps = 0.5):
        bins = self.create_bins()
        state = self.get_state_as_string(self.assign_bins(observation, bins))
        if np.random.uniform() < eps:
            return self.env.action_space.sample()
        else:
            return self.max_dict(Q[state])[0]

class GymAgent(object):
    """The world's simplest agent!"""
    def __init__(self,env_gym):
        self.env = gym.make(env_gym)
        self.env_name = env_gym
        # self.Q_algo = QLearning(self.env_name)
        # self.Q = self.Q_algo.initialize_Q()

    def act(self, observation, reward, done):

        #action = self.Q_algo.Q_act(self.Q,observation)
        #return action
        return self.env.action_space.sample()


