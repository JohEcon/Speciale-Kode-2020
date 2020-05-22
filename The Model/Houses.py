from dream_agent import Agent
from Settings import *
import random, math, numpy, matplotlib.pyplot as plt

class Houses(Agent):
    def __init__(self, parent=None, square_meters=0, quality=0, owner=0, price=0):
        super().__init__(parent)
        self._square_meters = square_meters
        self._quality = quality
        self._owner = owner
        self._price = price

    def get_quality(self):
        return self._quality

    def event_proc(self, id_event):
        if id_event == Event.start:
            self._quality = random.uniform(0, 1)
            self._square_meters = random.uniform(50, 400)