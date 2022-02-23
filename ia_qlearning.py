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

def detect_front(front):
    if front is not None and front[0] == 144:
        return 1
    elif front is not None and front[0] == 370:
        return 2

Q = np.zeros([3 , 3])
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

            # Get front
            front = detect_front(state)

            if front:
                action = np.argmax(Q[front])

                # If Q line is empty, choose random
                if Q[front][action] == 0:
                    action = random.randint(0, 2)

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
                
                reward = mario.fitness - before_reward

                Q[front][action] = Q[front][action] + 0.1 * (reward + 0.9 * np.max(Q[front]) - Q[front][action])
                print('Qtable : ', Q)
            else:
                pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
                pyboy.tick()
                pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        else:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            pyboy.tick()
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    mario.reset_game()

    print("Score: " + str(mario.fitness))

# 144 petit champi
# 370 tuyau