# TetrisAgent
Intelligent agent for Tetris
Currently supports 2 random agents for ALE platform and gym-tetris.

ALE platform source code: 
https://github.com/mgbellemare/Arcade-Learning-Environment

Gym-tetris source code:
https://github.com/Kautenja/gym-tetris

# Installation
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
