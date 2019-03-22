import gym_tetris
import timeit

env=gym_tetris.make("Tetris-v0")
start = timeit.default_timer()
for i in range(1000):
    env.reset()
    done = False
    step=0
    while not done:
        #access to the game board
        print(env.env.game.board)
        step+=1
        env.render('human')
        state, reward, done, info = env.step(env.action_space.sample())
    print(step)
stop = timeit.default_timer()
print('Time: ', stop - start)  



