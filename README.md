# TetrisAgent
-Intelligent agent for Tetris

-Supports intelligent agent for gym-tetris environment.

Gym-tetris source code:
https://github.com/Kautenja/gym-tetris

# Gym-tetris installation
Use your version of pip to install gym-tetris.

```shell
pip install gym-tetris
```
or
```shell
pip3 install gym-tetris
```
# Run with command line
```shell
gym_tetris -e <the environment ID to play> -m <`human` or `random`>
```

**NOTE:** by default, `-e` is set to `Tetris-v0` and `-m` is set to
`human`.

# Using intelligent agent
Paste this repository files inside the gym-tetris installation folder.

Run gym_test.py file to see the agent playing the game.
```shell
python gym_test.py
```

Inside gym_test.py file you can change weights for agent.
