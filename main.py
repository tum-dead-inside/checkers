import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import random

import matplotlib.pyplot as plt
import numpy as np


state_space = [State(i) for i in range(18)]
start_board = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1]

actions = [Action(i) for i in range(2)]
transition_model = TransitionModel()
reward_model = RewardModel()
initial_state = states[0]

mdp = MDP(states, actions, transition_model, reward_model, initial_state)
solver = Solver(mdp)
solver.solve()

def initialize_board():
    # 1 and -1 represent the pieces of two players 1 and -1
    board = np.zeros((6, 6))
    for i in range(2):
        for j in range(0, 6, 2):
            board[i][j + (i % 2)] = 1
            board[6 - i - 1][j + (i % 2)] = -1
    return board