import random
from pyboy import PyBoy, WindowEvent
import gym
import numpy as np

filename = 'mario.gb'
pyboy = PyBoy(filename, game_wrapper=True)

# PyBoyGymEnv
mario = pyboy.game_wrapper()
mario.start_game()
pyboy.set_emulation_speed(5)
env = pyboy.openai_gym()

Q = np.zeros([99999, 3])

# Do QLearning
for episode in range(2):
    print("Episode: ", episode)
    pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
    while mario.lives_left > 0:
        # Get State
        state = mario.fitness
        # Get Action
        action = np.argmax(Q[state])
        # Do Action
        if action == 0:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif action == 1:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif action == 2:
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        # Get Reward
        reward = mario.fitness - state
        # Get Next State
        next_state = mario.fitness
        # Update Q
        Q[state][action] = Q[state][action] + 0.1 * (reward + 0.9 * np.max(Q[next_state]) - Q[state][action])
        # Print out current state
        print("State: " + str(state) + " | Action: " + str(action) + " | Reward: " + str(reward) + " | Next State: " + str(next_state))
    mario.reset_game()

    print("Score: " + str(mario.fitness))
np.savetxt("qtable.csv", Q, delimiter=",")
        