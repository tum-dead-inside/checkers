# Introduction
This project dives into the world of Reinforcement Learning (RL) to develop an AI agent that dominates the classic American Checkers game. We'll be using Q-Learning to train our AI.

# Rules
- Players alternate turns and can only move their pieces diagonally forward to an adjacent unoccupied square
- To capture an opponent’s piece, a player must jump over it to an empty square immediately beyond it
- Multiple jumps are allowed in a single turn if after each jump there is another piece that can be captured
- If a player is able to make a capture, they must do so

# Simplifications Made
- No "kinged" pieces
- 6x6 board instead of 8x8