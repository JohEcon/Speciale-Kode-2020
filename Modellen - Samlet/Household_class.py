from dream_agent import Agent
from Settings import *
class Households(Agent):
    def __init__(self, parent=None, Wealth=0, Pdeath=0, Income=0, Age=Settings.starting_age, Dead=0):
        super().__init__(parent)
        self._Wealth = Wealth
        self._Income = Income
        self._Age = Age
        self._Pdeath = Pdeath
        self._Dead = Dead

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
        return "Household(ID: {}, Wealth: {}, Income: {}, Age: {}, p-death: {} )".format(self._id, self._Wealth,
                                                                                         self._Income, self._Age,
                                                                                         self._Pdeath)

    def event_proc(self, id_event):
        if id_event == Event.update:  # 2

            # if income is too low and household is young, set income to SU-level
            if self._Age == Settings.starting_age and self._Income < Settings.starting_income:
                self._Income = Settings.starting_income * (1 + numpy.random.normal(0, 0.1))

            if self._Age > Settings.starting_age and self._Income < 6200:
                self._Income = 6200

            if self._Age >= 30 and self._Income < 11500:
                self._Income = 11500

            # every year, increase age by 1 and update income
            if Simulation.time % Settings.periods_in_year == 0:
                self._Age += 1
                self._Pdeath = 0.0005 + 10 ** (-4.2 + 0.038 * self._Age)

                if self._Age < Settings.retire_age:
                    self._Income += dict_income_raise[get_index(self._Age)]
                    self._Income = self._Income * (
                        math.exp(numpy.random.normal(0, 0.113) + numpy.random.normal(0, 0.155)))

                if random.uniform(0, 1) < self._Pdeath:
                    print("Death of agent ID: {}, age: {}, period: {}".format(self._id, self._Age, Simulation.time))
                    deaths_period.append(Simulation.time)
                    self._Dead = 1
                    self.remove_this_agent()

                if self._Age > 109:
                    print("Death of agent ID: {}, age: {}, period: {}".format(self._id, self._Age, Simulation.time))
                    deaths_period.append(Simulation.time)
                    self._Dead = 1
                    self.remove_this_agent()

        elif id_event == Event.stop:  # 3

            print(repr(self))
