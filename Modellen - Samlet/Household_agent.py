from dream_agent import Agent
from Simulation import Simulation
from Simulation import Settings

class Households(Agent):
    def __init__(self, parent=None, Wealth=0, Income=0, Age=0):
        super().__init__(parent)
        self._Wealth = Wealth
        self._Income = Income
        self._Age = Age

    # Report Wealth
    def get_Wealth(self):
        return self._Wealth

     # Report Income
    def get_Income(self):
        return self._Income

    # Report Age
    def get_age(self):
        return self._Age

    # We define the string representation of the class objects
    def __repr__(self):
        return "Household(ID: {}, Wealth: {}, Income: {}, Age: {}, p-death: {} )".format(self._id, self._Wealth, self._Income, self._Age, self._Pdeath)

    def event_proc(self, id_event):
        if id_event == Event.update:  # 2
            if Simulation.time % Settings.periods_in_year == 0:
                self._Age += 1
                self._Pdeath = dict_death[self._Age]

            if random.uniform(0,1)<self._Pdeath:
                print("death of agent")
                self.remove_this_agent()

        elif id_event == Event.stop:  # 3
            print(repr(self))
