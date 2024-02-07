# Introduction
This is the code for a simple checkers game for our RL project. The game is played by two players, one of which is the user and the other is the AI. The AI uses Deep Q Learning to make its moves.

# Showcase

<p align="center">
  <img src="https://github.com/tum-dead-inside/checkers/assets/44473782/ee2f6ac6-d401-4628-a1de-1310ebeb4b8e" alt="image">
</p>

# How to Run

In order to run the game, you will need to have Python 3.10+ installed on your machine, as well as a couple dependencies which can be found in the requirements.txt file. To install these dependencies, simply run the following command in your terminal:

```sh
pip install -r requirements.txt
```

Alternatively for nix users, you can use the following command to use a temporary shell with the dependencies and python installed:

```sh
nix-shell
```

To run the game, simply run the `main.py` file. This will start the game and you can play against the AI.

```sh
python3 main.py
```

# Rules
- Players alternate turns and can only move their pieces diagonally forward to an adjacent unoccupied square
- To capture an opponent’s piece, a player must jump over it to an empty square immediately beyond it
- Multiple jumps are allowed in a single turn if after each jump there is another piece that can be captured
- If a player is able to make a capture, they must do so

# Simplifications Made
- No "kinged" pieces
- 6x6 board instead of 8x8 (this can be changed in the code in the `checkers/constants.py` file)

# Credits
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
