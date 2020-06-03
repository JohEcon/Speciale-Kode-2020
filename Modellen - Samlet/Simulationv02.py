# We import the DREAM agent
from dream_agent import Agent
from Dictionaries import *
import random, math, numpy, matplotlib.pyplot as plt
import statistics
from Settings import *

# We allocate an agent object
Model = Agent()

# We define the Households object
deaths_period = []


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


class Bank(Agent):
    pass


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


class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:
            self._file = open(Settings.statistics_file, "w")

            # Initialize graphics
            if Settings.graphics_show == True:
                plt.ion()
                plt.figure(figsize=[5, 5])

        elif id_event == Event.stop:
            self._file.close()

        elif id_event == Event.period_start:
            print(Simulation.time)

            if Settings.graphics_show == True:
                if Simulation.time % Settings.graphics_periods_per_pic == 0:
                    # Gather data from population
                    w = []
                    for p in Simulation.Household:
                        w.append(p.income)

                    # Display data
                    plt.clf()
                    plt.hist(w, bins=100, color="blue")
                    plt.axis(xmin=6200, xmax=100000)
                    plt.title("Distribution of wealth ({})".format(Simulation.time))
                    plt.show()
                    plt.pause(0.000001)


class Simulation(Agent):
    # Static fields
    Household = Agent()
    time = 1

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents
        # Children of simulation:

        Simulation.Houses = Agent(self)
        self._statistics = Statistics(self)
        Simulation.Household = Agent(self)

        for i in range(Settings.number_of_agents):
            Households(Simulation.Household)

        for i in range(10):
            Houses(Simulation.Houses)

        # Start the simulation
        self.event_proc(Event.start)

    def event_proc(self, id_event):
        if id_event == Event.start:  # 6
            # Send Event.start down the tree to all decendants
            super().event_proc(id_event)  # 7

            # The Event Pump: the actual simulation      #8
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.period_start)
                self.event_proc(Event.update)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.stop)  # 9


        elif id_event == Event.update:  # 10

            # Adding new born persons to the population
            for i in range(int(deaths_period.count(Simulation.time - 1))):
                Households(Simulation.Household)
                print("agent added - Age: , Income: , Period: {}".format(Simulation.time))
            super().event_proc(id_event)
        else:
            # All other events are sendt to decendants
            super().event_proc(id_event)


Simulation()

all_houses_quality = []
all_incomes = []
all_ages = []
total_income = 0

for n in Simulation.Houses:
    all_houses_quality.append(n.get_quality())

for n in Simulation.Household:
    all_incomes.append(n.income)

for n in Simulation.Household:
    all_ages.append(n.age)

for value in all_incomes:
    total_income += value

average_income = total_income / Simulation.Household.number_of_agents()
median_income = statistics.median(all_incomes)
# print(Simulation.Household.number_of_agents())
# print(total_income)
# print(average_income)
# print(deaths_period)
# print(all_incomes)
print(median_income)
print(average_income)
all_incomes = []
for n in Simulation.Household:
    all_incomes.append(n.income)

for value in all_incomes:
    total_income += value

print(all_ages)
# all_incomes = [i for i in all_incomes if i != 11500]


plt.hist(all_incomes, bins=2500, color="blue")
plt.axis(xmin=-10000, xmax=150000)
plt.show()

plt.hist(all_ages, bins=dict_bin_ages2, color="blue")
plt.axis(xmin=20, xmax=110)
plt.show()
