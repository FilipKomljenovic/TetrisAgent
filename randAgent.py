import sys
import timeit
from random import randrange
from ale_python_interface import ALEInterface

if len(sys.argv) < 2:
  print('Usage: %s rom_file' % sys.argv[0])
  sys.exit()

ale = ALEInterface()
ale.setInt(b'random_seed', 123)
ale.setBool('display_screen',True)

rom_file = str.encode(sys.argv[1])
ale.loadROM(rom_file)
legal_actions = ale.getLegalActionSet()
start = timeit.default_timer()

#Play 1000 episodes
for episode in range(1000):
  total_reward = 0
  step=0
  while not ale.game_over():
    step+=1
    a = legal_actions[randrange(len(legal_actions))]
    reward = ale.act(a);
    total_reward += reward
  print('Steps for this game:',step)
  ale.reset_game()

stop = timeit.default_timer()
print('Time played for 1000 episodes: ', stop - start)
