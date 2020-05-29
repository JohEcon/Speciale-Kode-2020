from dream_agent import *
from Settings import *

class Bank(Agent):
    def __init__(self, parent = None, interest = Settings.interest):
        super().__init__(parent)
        self._interest = interest

    def get_interest(self):
        return self._interest

    def max_loan_household(self, age, income, duration, periods):
        piti=income*Settings.piti_multiplier

        max_loan = (piti*(1-(1+self._interest/periods)**(-(duration*periods))))/(self._interest/periods)
        return max_loan

danske_bank = Bank()