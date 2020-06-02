from dream_agent import Agent
from Settings import *
import random, math, numpy, matplotlib.pyplot as plt

class Houses(Agent):
    def __init__(self, parent = None, square_meters = 0, quality = 0, owner = None, price = 0, for_sale = True, seller = None):
        super().__init__(parent)
        self._square_meters = square_meters
        self._quality = quality
        self._owner = owner
        self._price = price
        self._for_sale = for_sale
        self._seller = seller

    def get_quality(self):
        return self._quality

    def get_for_sale(self):
        return self._for_sale

    def get_owner(self):
        return self._owner

    def get_price(self):
        return self._price

    def get_seller(self):
        return self._seller

    def event_proc(self, id_event):
        if id_event == Event.start:
            self._quality = random.uniform(0, 1)
            self._square_meters = random.uniform(50, 400)
            self._price = self._quality*2500000

    def setting_owner(self, owner_id):
        self._owner=owner_id

    def setting_seller(self, seller):
        self._seller = seller

    def setting_for_sale(self, seller):
        self._for_sale = True
        self._seller = seller


    def unlisting_house(self):
        self._for_sale = False
        print("unlisting house: {}, for sale: {}".format(self.get_id(), self.get_for_sale()))

    def set_price(self, price):
        self._price = price
        print("House {} price set to {}". format(self.get_id(), self._price))