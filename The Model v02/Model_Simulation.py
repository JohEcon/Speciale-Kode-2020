# We import the DREAM agent
from Houses import *
from Bank import *
import random, math, numpy
from Data import *
from Statistics import *
# We allocate an agent object
Model = Agent()


class Household(Agent):

    def __init__(self, parent=None, wealth= 0, pdeath = 0, income = 0, age = Settings.starting_age, house_owned = None, dead = False, died_last_period = False, moving = False, max_loan = 0):
        super().__init__(parent)
        self._wealth = wealth
        self._income = income
        self._age = age
        self._pdeath = pdeath
        self._dead = dead
        self._died_last_period = died_last_period
        self._moving = moving
        self._house_owned = house_owned
        self._max_loan = max_loan

    def get_wealth(self):
        return self._wealth

    def get_house_owned(self):
        return self._house_owned

    # Report Income
    def get_income(self):
        return self._income

    # Report Age
    def get_age(self):
        return self._age

    #report if dead
    def get_dead(self):
        return self._dead

    def get_died_last_period(self):
        return self._died_last_period
    # We define the string representation of the class objects
    def __repr__(self):
        return "Household(ID: {}, Wealth: {}, Income: {}, Age: {}, House ID: {} p-death: {}, dead: {} )".format(self._id, self._wealth,
                                                                                         round(self._income), self._age, self._house_owned,
                                                                                         round(self._pdeath, 5), self._dead)

    def event_proc(self, id_event):
        #checking if household is dead
        if self._dead == True:
            self._died_last_period = False

        #initiating behaviour of living household
        if self._dead == False:

            if id_event == Event.start:
                pass

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
                if random.uniform(0,1) < 0.01 and self._moving == False:
                    first = True
                    self._moving = True
                    #Asking the bank how much the largest possible loan the household can get is (Budget constraint)
                    self._max_loan = Bank.max_loan_household(Simulation.Banks.get_random_agent(), self._age, self._income, Settings.loan_lenght,
                                        Settings.periods_in_year)
                    #if already house owner, set own house for sale
                    for n in Simulation.Houses:
                        if n.get_id() == self._house_owned:
                            print(n.get_for_sale())
                            n.setting_for_sale()
                            print(n.get_for_sale())
                        else:
                            pass
                    #Finding the best house given budget
                    for n in Simulation.Houses:
                        if n.get_for_sale() == True and self._max_loan >= n.get_price():
                            if first == True:
                                best_house = n
                                first = False
                            if n.get_quality() > best_house.get_quality():
                                best_house = n
                                #print("new best house {}".format(best_house.get_id()))
                            else:
                                pass
                    #unlisting new house
                    if first == False:
                        best_house.setting_owner(self.get_id())
                        self._house_owned = best_house.get_id()
                        best_house.unlisting_house()
                        #print("own id: {}, house id: {}, house quality: {}".format(self.get_id(), self._house_owned, round(best_house.get_quality(), 4)))
                        #print(self._house_owned)
                        #stopping moving process
                        self._moving = False

            if id_event == Event.update_year:
            # every year, increase age by 1 and update income
                self._age += 1
                self._pdeath = prop_death(self._age)

                if self._age < Settings.retire_age:
                    self._income += dict_income_raise[get_index(self._age)]
                    self._income = self._income * (math.exp(numpy.random.normal(0, 0.113) + numpy.random.normal(0, 0.155)))

                if random.uniform(0, 1) < self._pdeath:
                    self._died_last_period = True
                    self._dead = True
                    # set house for sale
                    for n in Simulation.Houses:
                        if n.get_id() == self._house_owned:
                            n.setting_for_sale()
                        else:
                            pass

                if self._age > Settings.max_age:
                    self._died_last_period = True
                    self._dead = True
                    # set house for sale
                    for n in Simulation.Houses:
                        if n.get_id() == self._house_owned:
                            n.setting_for_sale()
                        else:
                            pass

            elif id_event == Event.stop:  # 3
                    print(repr(self))


class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:                     #1
            self._file = open(Settings.out_file, "w")
            self._file.write("dict_deaths_period={}")
        elif id_event == Event.stop:                    #2
            self._file.close()

        elif id_event == Event.period_start:            #3
            for n in Simulation.Households:
                if n.get_died_last_period() == 1:
                    deaths_period.append(Simulation.time)
                else:
                    pass
            dict_deaths_period[Simulation.time-1]=int(deaths_period.count(Simulation.time))

class Simulation(Agent):
    # Static fields
    Households = Agent()
    time = 1

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents
        # Children of simulation:
        Simulation.Banks = Agent(self)
        Simulation.Houses = Agent(self)
        self._statistics = Statistics(self)
        Simulation.Households = Agent(self)

        for i in range(Settings.number_of_banks):
            Bank(Simulation.Banks)

        for i in range(Settings.number_of_agents):
            Household(Simulation.Households)

        for i in range(Settings.number_of_houses):
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
                if Simulation.time % Settings.periods_in_year == 0:
                    self.event_proc(Event.update_year)
                Simulation.time += 1


            # Stop the simulation
            self.event_proc(Event.stop)  # 9


        elif id_event == Event.period_start:  # 10
            # Adding new born persons to the population
            super().event_proc(id_event)
            for i in range(dict_deaths_period[Simulation.time-1]):
                Household(Simulation.Households)

        else:
            # All other events are sent to decendants
            super().event_proc(id_event)

#We run the simulation
Simulation()
