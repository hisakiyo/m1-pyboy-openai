import random
from pyboy import PyBoy, WindowEvent

filename = 'mario.gb'
pyboy = PyBoy(filename, game_wrapper=True)

mario = pyboy.game_wrapper()
mario.start_game()
pyboy.set_emulation_speed(1)

pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
while mario.lives_left >= 0:
    action = random.randint(0, 1)
    
    if action == 0:
        pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        for _ in range(10):
            pyboy.tick()
        pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    elif action == 1:
        pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        pyboy.tick()
        pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
else:
    print("Mario dead.")
    exit(2)

mario.reset_game()

pyboy.stop()
