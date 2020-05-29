from dream_agent import Agent
from Settings import *
import random, math, numpy, matplotlib.pyplot as plt

class Houses(Agent):
    def __init__(self, parent=None, square_meters=0, quality=0, owner="none", price=0, for_sale=True):
        super().__init__(parent)
        self._square_meters = square_meters
        self._quality = quality
        self._owner = owner
        self._price = price
        self._for_sale = for_sale

    def get_quality(self):
        return self._quality

    def get_for_sale(self):
        return self._for_sale

    def get_price(self):
        return self._price

    def event_proc(self, id_event):
        if id_event == Event.start:
            self._quality = random.uniform(0, 1)
            self._square_meters = random.uniform(50, 400)
            self._price = self._quality*1500000

    def setting_owner(self, owner_id):
        print("old owner: {}, own id:{}, quality: {}".format(self._owner, self.get_id(), round(self.get_quality(),4)))
        self._owner=owner_id
        print("new owner: {}, own id:{}, quality: {}".format(self._owner, self.get_id(), round(self.get_quality(),4)))

    def setting_for_sale(self):
        self._for_sale = True
        print("listing house: {}, for sale: {}".format(self.get_id(), self.get_for_sale()))

    def unlisting_house(self):
        self._for_sale = False
        print("unlisting house: {}, for sale: {}".format(self.get_id(), self.get_for_sale()))

    def set_price(self, price):
        self._price = price
        print("House {} price set to {}". format(self.get_id(), self._price))