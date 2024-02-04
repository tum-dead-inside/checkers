import torch
import torch.nn as nn
import random
from checkers.experience import Experience


class DQN(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        """
        Initializes a DQN (Deep Q-Network) model.

        Args:
            input_size (int): The size of the input tensor.
            output_size (int): The size of the output tensor.
        """
        super(DQN, self).__init__()
        self.fc = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, output_size)

    def forward(self, x):
        """
        Performs a forward pass through the DQN model.

        Args:
            x: The input tensor.

        Returns:
            The output tensor.
        """
        x = torch.relu(self.fc(x))
        x = self.fc2(x)
        return x


class ReplayBuffer:
    def __init__(self, capacity):
        """
        Initialize the ReplayBuffer object.

        Args:
            capacity (int): The maximum capacity of the buffer.
        """
        self.buffer = []
        self.capacity = capacity

    def push(self, experience):
        """
        Add an experience to the buffer.

        If the buffer is already at maximum capacity, the oldest experience will be removed.

        Args:
            experience (object): The experience to be added to the buffer.
        """
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(experience)

    def sample(self, batch_size):
        """
        Randomly sample experiences from the buffer.

        Args:
            batch_size (int): The number of experiences to sample.

        Returns:
            list: A list of sampled experiences.
        """
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        """
        Get the current size of the buffer.

        Returns:
            int: The number of experiences in the buffer.
        """
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

    # convert states, actions, rewards, and next_states to tensors
    state_batch = torch.tensor(batch.state, dtype=torch.float32)
    action_batch = torch.tensor(batch.action, dtype=torch.long)
    reward_batch = torch.tensor(batch.reward, dtype=torch.float32)
    next_state_batch = torch.tensor(batch.next_state, dtype=torch.float32)

    current_q_values = dqn(state_batch)  # get current Q-values
    next_q_values = (
        dqn(next_state_batch).max(dim=1).values.detach()
    )  # get next Q-values and detach from computation graph

    target_q_values = reward_batch + gamma * next_q_values  # calculate target Q-values

    loss = nn.MSELoss()(
        current_q_values.gather(
            dim=1, index=action_batch.unsqueeze(dim=1)
        ),  # gather Q-values for selected actions
        target_q_values.unsqueeze(dim=1),
    )

    optimizer.zero_grad()  # zero the gradients
    loss.backward()  # backpropagate the loss
    optimizer.step()  # update the model's parameters
