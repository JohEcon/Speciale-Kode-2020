
from Bank import *
import random, math, numpy
from Data import *

class Household(Agent):

    def __init__(self, parent=None, wealth= 0, pdeath = 0, income = 0, age = Settings.starting_age, dead = 0, died_this_period = 0, moving = 0):
        super().__init__(parent)
        self._wealth = wealth
        self._income = income
        self._age = age
        self._pdeath = pdeath
        self._dead = dead
        self._died_this_period = died_this_period
        self._moving = moving

    def get_wealth(self):
        return self._wealth

    # Report Income
    def get_income(self):
        return self._income

    # Report Age
    def get_age(self):
        return self._age

    #report if dead
    def get_dead(self):
        return self._dead

    def get_died_this_period(self):
        return self._died_this_period
    # We define the string representation of the class objects
    def __repr__(self):
        return "Household(ID: {}, Wealth: {}, Income: {}, Age: {}, p-death: {}, dead: {} )".format(self._id, self._wealth,
                                                                                         self._income, self._age,
                                                                                         self._pdeath, self._dead)

    def event_proc(self, id_event):
        #checking if household is dead
        if self._dead == 1:
            self._died_this_period = 0

        #initiating behaviour of living household
        if self._dead == 0:
            if id_event == Event.period_start:
                pass

            if id_event == Event.update:  # 2
            # if income is too low and household is young, set income to SU-level
                if self._age == Settings.starting_age and self._income < Settings.starting_income:
                    self._income = Settings.starting_income * (1 + numpy.random.normal(0, 0.1))

                if self._age > Settings.starting_age and self._income < Settings.su_income:
                    self._income = Settings.su_income

                if self._age >= 30 and self._income < Settings.kh_income:
                    self._income = Settings.kh_income

            #check if household wants to move, if so, initiate moving procedure
                if random.uniform(0,1) < 0.01:
                    #Asking the bank how much the largest possible loan the household can get is (Budget constraint)
                    print(Bank.max_loan_household(Simulation.Banks.get_random_agent(self), self._age, self._income, Settings.loan_lenght,
                                        Settings.periods_in_year))
                    #best_house = Simulation.Houses.get_random_agent(self)


            if id_event == Event.update_year:
            # every year, increase age by 1 and update income
                self._age += 1
                self._pdeath = prop_death(self._age)

                if self._age < Settings.retire_age:
                    self._income += dict_income_raise[get_index(self._age)]
                    self._income = self._income * (math.exp(numpy.random.normal(0, 0.113) + numpy.random.normal(0, 0.155)))

                if random.uniform(0, 1) < self._pdeath:
                    self._died_this_period = 1
                    self._dead = 1

                if self._age > Settings.max_age:
                    self._died_this_period = 1
                    self._dead = 1

            elif id_event == Event.stop:  # 3
                    print(repr(self))

