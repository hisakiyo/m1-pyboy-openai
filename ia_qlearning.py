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

Q = np.zeros([10000, 10000, 3])
print(Q)
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
            print(Q[state[0]])
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
            elif action == 2:
                pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
                pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
            # Get Reward
            reward = mario.fitness - before_reward
            # Get Next State
            next_state = find_case_front_mario(np.asarray(mario.game_area()))
            #print("State: ", state)
            #print("Next state: ", next_state)

            if next_state is not None:
                # if next_state[0] == 144:
                #     Q[state[0]][state[1]][action] = reward + 1
                # elif next_state[0] == 370:
                #     Q[state[0]][state[1]][action] = reward + 1
                # else:
                Q[state[0]][state[1]][action] = Q[state[0]][state[1]][action] + 0.1 * (reward + 0.9 * np.max(Q[next_state[0]][next_state[1]]) - Q[state[0]][state[1]][action])
            else:
                pyboy.tick()
        else:
            pyboy.tick()
    mario.reset_game()

    print("Score: " + str(mario.fitness))
    print(Q)
    # save Q in csv file
    #np.savetxt("Q.csv", Q, delimiter=",")

# 144 petit champi
# 370 tuyau