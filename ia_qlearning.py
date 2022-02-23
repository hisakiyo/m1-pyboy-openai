import random
from pyboy import PyBoy, WindowEvent
import gym
import numpy as np
import os

filename = 'mario.gb'
pyboy = PyBoy(filename, game_wrapper=True)

# PyBoyGymEnv
mario = pyboy.game_wrapper()
mario.start_game()
pyboy.set_emulation_speed(5)

# Find ajacent case in the array of the cell with 17
def find_case_front_mario(game_area):
    for i in range(len(game_area)):
        for j in range(len(game_area[i])):
            if game_area[i][j] > 10 and game_area[i][j] < 30 and game_area[i][j] % 2 == 1:
                return [game_area[i, j+1], game_area[i-1, j+1]]

# Read qtable.csv into a numpy array
# if qtable.csv exists
# if os.path.isfile('qtable.csv'):
#     Q = np.loadtxt('qtable.csv', delimiter=',')
# else:
#     Q = np.zeros([1000, 2])
Q = np.zeros([10000, 10000, 2])
# Do QLearning
for episode in range(100):
    print("Episode: ", episode)
    pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
    while mario.lives_left > 0:
        # Get State
        state = find_case_front_mario(np.asarray(mario.game_area()))
        if state is not None:
            before_reward = mario.fitness
            # Get Action
            action = np.argmax(Q[state[0]][state[1]])
            # Do Action
            if action == 0:
                pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
                pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
            elif action == 1:
                pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
                for _ in range(10):
                    pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
            # Get Reward
            reward = mario.fitness - before_reward
            # Get Next State
            next_state = find_case_front_mario(np.asarray(mario.game_area()))
            if next_state is not None:
                Q[state[0]][state[1]][action] = Q[state[0]][state[1]][action] + 0.1 * (reward + 0.9 * np.max(Q[next_state[0]][next_state[1]]) - Q[state[0]][state[1]][action])
            else:
                pyboy.tick()
        else:
            pyboy.tick()
    mario.reset_game()

    print("Score: " + str(mario.fitness))