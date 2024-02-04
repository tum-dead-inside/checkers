import torch
import torch.nn as nn
import random
from checkers.experience import Experience


class DQN(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super(DQN, self).__init__()
        self.fc = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.relu(self.fc(x))
        x = self.fc2(x)
        return x


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity

    def push(self, experience):
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(experience)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


def train_dqn(dqn, replay_buffer, batch_size, gamma, optimizer):
    """
    Trains a DQN (Deep Q-Network) model using the given replay buffer, batch size, discount factor (gamma),
    and optimizer.

    Args:
        dqn (torch.nn.Module): The DQN model to train.
        replay_buffer (ReplayBuffer): The replay buffer containing the experiences.
        batch_size (int): The number of experiences to sample from the replay buffer for each training iteration.
        gamma (float): The discount factor for future rewards.
        optimizer (torch.optim.Optimizer): The optimizer used to update the DQN model's parameters.

    Returns:
        None
    """
    if len(replay_buffer) < batch_size:
        return

    experiences = replay_buffer.sample(batch_size)
    batch = Experience(*zip(*experiences))

    state_batch = torch.tensor(batch.state, dtype=torch.float32)
    action_batch = torch.tensor(batch.action, dtype=torch.long)
    reward_batch = torch.tensor(batch.reward, dtype=torch.float32)
    next_state_batch = torch.tensor(batch.next_state, dtype=torch.float32)

    current_q_values = dqn(state_batch)
    next_q_values = dqn(next_state_batch).max(dim=1).values.detach()

    target_q_values = reward_batch + gamma * next_q_values

    loss = nn.MSELoss()(
        current_q_values.gather(dim=1, index=action_batch.unsqueeze(dim=1)),
        target_q_values.unsqueeze(dim=1),
    )

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
