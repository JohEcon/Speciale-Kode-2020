# We import the DREAM agent
from dream_agent import Agent
from Dictionaries import *

import random
import numpy

# We allocate an agent object
Model = Agent()

class Settings: pass
Settings.number_of_agents=10
Settings.number_of_periods=600
Settings.fraction_of_new_born=0.0
Settings.periods_in_year=12
Settings.starting_income=9500
Settings.starting_age= 20

# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.update = 3  # Agent behavior

# We define the Households object
deaths_period = []

class Households(Agent):
    def __init__(self, parent=None, Wealth=0, Pdeath=0, Income=Settings.starting_income, Age=Settings.starting_age):
        super().__init__(parent)
        self._Wealth = Wealth
        self._Income = Income
        self._Age = Age
        self._Pdeath = Pdeath


    # Report ID
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
            #add income to total wealth
            self._Wealth += self._Income

            #every year, increase age by 1 and update income
            if Simulation.time % Settings.periods_in_year == 0:
                self._Age += 1
                self._Pdeath = 0.0005+10**(-4.2+0.038*self._Age)
                self._Income += dict_income_raise[get_index(self._Age)]
                self._Income +=self._Income*(numpy.random.normal(0, 0.113)+numpy.random.normal(0, 0.155))

                #if income is too low and household is young, set income to SU-level
                if self._Age <30 and self._Income <6200:
                    self._Income = 6200

                #if income is too low and household is old, set income to unemplyment benefit level
                if self._Age >=30 and self._Income <11500:
                    self._Income = 11500

                if random.uniform(0,1)<self._Pdeath:
                    print("Death of agent ID: {}, age: {}, period: {}".format(self._id, self._Age, Simulation.time))
                    deaths_period.append(Simulation.time)
                    self.remove_this_agent()

                if self._Age > 109:
                    print("Death of agent ID: {}, age: {}, period: {}".format(self._id, self._Age, Simulation.time))
                    deaths_period.append(Simulation.time)
                    self.remove_this_agent()

        #elif id_event == Event.stop:  # 3
            #print(repr(self))



class Simulation(Agent):
    # Static fields
    Household = Agent()
    time = 1

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents
        # Simulation has 1 child:
        Simulation.Household = Agent(self)

        for i in range(Settings.number_of_agents):
            Households(Simulation.Household)

        # Start the simulation
        self.event_proc(Event.start)

    def event_proc(self, id_event):
        if id_event == Event.start:  # 6
            # Send Event.start down the tree to all decendants
            super().event_proc(id_event)  # 7

            # The Event Pump: the actual simulation      #8
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.update)
                Simulation.time += 1


            # Stop the simulation
            self.event_proc(Event.stop)  # 9


        elif id_event == Event.update:  # 10
                # Adding new born persons to the population
            for i in range(int(round(Settings.fraction_of_new_born*Simulation.Household.get_number_of_agents()))):
                Households(Simulation.Household)
                print("agent added - Age: {}, Income: {}")
            super().event_proc(id_event)
        else:
                # All other events are sendt to decendants
            super().event_proc(id_event)

Simulation()

all_incomes = []
total_income=0
for n in Simulation.Household:
    all_incomes.append(n.get_Income())

for value in all_incomes:
    total_income += value

average_income = total_income/Simulation.Household.number_of_agents()

print(Simulation.Household.number_of_agents())
print(total_income)
print(average_income)
print(deaths_period)

all_incomes = []
for n in Simulation.Household:
    all_incomes.append(n.get_Income())

for value in all_incomes:
    total_income += value

