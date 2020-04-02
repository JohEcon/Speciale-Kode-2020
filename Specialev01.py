# We import the DREAM agent
from dream_agent import Agent
from Dictionaries import dict_death
import random

# We allocate an agent object
Model = Agent()

# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.update = 3  # Agent behavior

# We define the Households object
class Households(Agent):
    def __init__(self, parent=None, Wealth=0, Income=0, Age=0, Pdeath=0):
        super().__init__(parent)
        self._Wealth = Wealth
        self._Income = Income
        self._Age = Age
        self._Pdeath= Pdeath

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
            if Simulation.time % Settings.periods_in_year == 0:
                self._Age += 1

            if random.uniform(0,1)<dict_death[self._Age]:
                print("death of agent")
                self.remove_this_agent()

        elif id_event == Event.stop:  # 3
            print(repr(self))

class Settings: pass
Settings.number_of_agents=0
Settings.number_of_periods=0
Settings.periods_in_year=0
Settings.fraction_of_new_born=0

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
                print(Simulation.Household.get_number_of_agents())

            # Stop the simulation
            self.event_proc(Event.stop)  # 9


        elif id_event == Event.update:  # 10
                # Adding new born persons to the population
            for i in range(int(round(Settings.fraction_of_new_born*Simulation.Household.get_number_of_agents()))):
                Households(Simulation.Household)
                print("agent added")
            super().event_proc(id_event)
        else:
                # All other events are sendt to decendants
            super().event_proc(id_event)

Settings.number_of_agents=10
Settings.number_of_periods=25
Settings.fraction_of_new_born=0.1
Settings.periods_in_year=12
Simulation()

