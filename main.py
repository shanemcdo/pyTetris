from game import game
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "15,30"

g = game(True)
g.printcontrols()
g.play()
