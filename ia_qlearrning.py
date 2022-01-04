import random
from pyboy import PyBoy, WindowEvent
import gym
import numpy as np

scale = 1
bootROM = None
filename = 'mario.gb'
pyboy = PyBoy(filename, game_wrapper=True)
# PyBoyGymEnv
mario = pyboy.game_wrapper()
mario.start_game()
pyboy.set_emulation_speed(1000)
env = pyboy.openai_gym()

# Q-table
print(mario.fitness)

episodes = 30
steps = 800
fitness_old = 0

actions = []
best_actions = []

for episode in range(episodes):
    # Fitness (score) is in mario.fitness
    print("Episode: ", episode)
    # Reset fitness
    pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
    while mario.lives_left > 1:
        action = env.action_space.sample()
        if action == 0:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif action == 1:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        elif action == 2:
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        elif action == 3:
            pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif action == 4:
            pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        elif action == 5:
            pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        # tick
        pyboy.tick()
        actions.append(action)
    print("Fitness: ", mario.fitness)
        
    # Store actions if fitness is higher than before
    if mario.fitness > fitness_old:
        best_actions = actions
        fitness_old = mario.fitness
        print("New fitness: ", fitness_old)

pyboy.set_emulation_speed(1)
print(len(best_actions))
# Play best actions
mario.reset_game()
pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
while mario.lives_left > 1:
        # pick first element in best_actions
        action = best_actions.pop(0)
        if action == 0:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif action == 1:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        elif action == 2:
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        elif action == 3:
            pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif action == 4:
            pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        elif action == 5:
            pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        # tick
        pyboy.tick()
print("Fitness: ", mario.fitness)
    