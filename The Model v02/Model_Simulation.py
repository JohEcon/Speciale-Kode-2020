# We import the DREAM agent
from dream_agent import *
from Settings import *
import random, math, numpy
from Data import *
from Statistics import *
# We allocate an agent object
Model = Agent()

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
        #print("unlisting house: {}, for sale: {}".format(self.get_id(), self.get_for_sale()))

    def set_price(self, price):
        self._price = price
        #print("House {} price set to {}". format(self.get_id(), self._price))

class Bank(Agent):
    def __init__(self, parent = None, interest = Settings.interest):
        super().__init__(parent)
        self._interest = interest

    @property
    def interest(self):
        return self._interest

    def max_loan_household(self, age, income, duration, periods):
        piti=income*Settings.piti_multiplier

        max_loan = (piti*(1-(1+self.interest/periods)**(-(duration*periods))))/(self.interest/periods)
        return max_loan

    def get_loan_household(self, principal, duration, periods):
        annuity = (principal*(self.interest/periods))/((1-(1+(self.interest/periods))**(-(duration*periods))))
        return annuity

danske_bank = Bank()



class Household(Agent):

    def __init__(self, parent=None, wealth = 0, pdeath = 0, income = 0, age = Settings.starting_age, house_owned = None, dead = False, died_last_period = False, moving = False, max_loan = 0):
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
        self._houses_bought = 0


    def get_houses_bought(self):
        return self._houses_bought

    # Report wealth
    @property
    def wealth(self):
        return self._wealth

    # Report id of owned house
    @property
    def house_owned(self):
        return self._house_owned

    # Report Income
    @property
    def income(self):
        return self._income

    # Report Age
    @property
    def age(self):
        return self._age

    #report if dead
    @property
    def dead(self):
        return self._dead

    @property
    def died_last_period(self):
        return self._died_last_period
    # We define the string representation of the class objects

    def communication(self, communicate, agent):
        if communicate == Communication.buy_house:
            #print("old owner: {}, own id:{}, quality: {}".format(agent.get_owner(), agent.get_id(),
                                                                 #round(agent.get_quality(), 4)))
            #buy house and transfer funds to owner (if owner exists)
            self._wealth += -agent.get_price()
            self._houses_bought += 1
            if agent.get_owner() != None:
                get_agent_with_id(Simulation.Households, agent.get_seller()).communication(Communication.sell_house, agent)
            else:
                pass
            #Set you as owner of house
            self._house_owned = agent.get_id()
            agent.setting_owner(self.get_id())
            #unlist house
            agent.unlisting_house()
            #print("new owner: {}, house id:{}, quality: {}".format(agent.get_owner(), agent.get_id(),
                                                                 #round(agent.get_quality(), 4)))

        if communicate == Communication.sell_house:
            #get money form purchase
            self._wealth += agent.get_price()
            #remove yourself as seller
            agent.setting_seller(None)
            #remove self as owner, if still owner
            if self.house_owned == agent.get_id():
                self._house_owned = None
            else:
                pass

    def __repr__(self):
        return "Household(ID: {a}, Wealth: {b}, Income: {c}, after_tax: {aa} Age: {d}, House ID: {e}, House quality: {f}, p-death: {g}, max loan: {h}, moving: {i}, houses bought: {j} )".format(a = self._id, b = round(self._wealth),
                                                                                         c = round(self._income), d = self._age, e = self._house_owned,
                                                                                         f = round(get_agent_with_id(Simulation.Houses, self._house_owned).get_quality() if get_agent_with_id(Simulation.Houses, self._house_owned) != None else 0, 4),
                                                                                         g = round(self._pdeath, 4), h = round(self._max_loan), i = self._moving, j= self._houses_bought, aa = round(pay_income_taxes(self._income)))

    def event_proc(self, id_event):
        #checking if household is dead
        #initiating behaviour of living household
        if id_event == Event.start:
            pass

        if id_event == Event.period_start:
            if self._dead == True:
                self._died_last_period = False

        if id_event == Event.update:  # 2
            if self._dead == False:
                #set starting income for newborn agents
                if self._age == Settings.starting_age and self._income < 1:
                    self._income = Settings.starting_income * (1 + numpy.random.normal(0, 0.1))

                #add income after tax to wealth
                self._wealth += pay_income_taxes(self._income)



            #check if household wants to move, if so, initiate moving procedure
                if random.uniform(0,1) < prop_moving(self.age) and self._moving == False:
                    #print("starting moving: {}, period: {}".format(self.get_id(), Simulation.time))
                    self._moving = True

                    #if already house owner, set own house for sale
                    if self._house_owned != None:
                        get_agent_with_id(Simulation.Houses, self.house_owned).setting_for_sale(self.get_id())
                        #print("own id: {}, listning: {}, period: {}".format(self.get_id(), self.house_owned, Simulation.time))
                    else:
                        pass

                if self._moving == True:
                    best_house = None
                    first = True
                    # Asking the bank how much the largest possible loan the household can get is (Budget constraint)
                    self._max_loan = Bank.max_loan_household(Simulation.Banks.get_random_agent(), self._age, self._income, Settings.loan_lenght, Settings.periods_in_year)
                    #Finding the best house given budget, agent can't buy their own house and agent wont move into a house worse than their current house
                    for n in Simulation.Houses:
                        if n.get_for_sale() == True and self._max_loan >= n.get_price() and n.get_id() != self._house_owned and self.get_id() != n.get_seller():
                            if first == True:
                                best_house = n
                                first = False
                                #print("new best house {}".format(best_house.get_id()))
                            if n.get_quality() > best_house.get_quality():
                                best_house = n
                                #print("new best house {}".format(best_house.get_id()))
                            else:
                                pass
                    if best_house == None:
                        pass
                        #print("No best house")

                    #buy the best house found:
                    if best_house != None:
                        self.communication(Communication.buy_house, best_house)
                        self._moving = False
                        #print("own id: {}, house id: {}, house quality: {}, period: {} \n".format(self.get_id(), self._house_owned, round(best_house.get_quality(), 4),Simulation.time))
                    else:
                        pass

                #check if agent dies
                if random.uniform(0, 1) < self._pdeath:
                    self._died_last_period = True
                    self._dead = True
                    print("agent {} dead, period: {}".format(self.get_id(), Simulation.time))
                    # set house for sale
                    for n in Simulation.Houses:
                        if n.get_id() == self._house_owned:
                            n.setting_for_sale(self.get_id())
                        else:
                            pass
                if self.died_last_period == 1:
                    print(Simulation.time)

        if id_event == Event.update_year:
            if self._dead == False:
                # every year, increase age by 1 and update income
                self._age += 1
                self._pdeath = prop_death(self._age)
                if self.died_last_period == 1:
                    print(Simulation.time)

                if self._age < Settings.retire_age:
                    self._income += dict_income_raise[get_index(self._age)]
                    self._income = self._income * (math.exp(numpy.random.normal(0, 0.113) + numpy.random.normal(0, 0.155)))

                if self._age == Settings.retire_age:
                    self._income = self._income*Settings.pension_share

                # if income is too low and household is young, set income to SU-level
                if self._age > Settings.starting_age and self._income < Settings.su_income:
                    self._income = Settings.su_income

                if self._age >= 30 and self._income < Settings.kh_income:
                    self._income = Settings.kh_income

                #if agent over max age, kill agent
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
            if self._dead == False:
                print(repr(self))


class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:                     #1
            self._file = open(Settings.out_file, "w")
            self._file.write("dict_deaths_period={}")
        elif id_event == Event.stop:                    #2
            self._file.close()

        elif id_event == Event.period_end:
            wealth = [h.wealth for h in Simulation.Households]
            income = [h.income for h in Simulation.Households]
            self.Statistiscs = [h.died_last_period for h in Simulation.Households]
            Settings.died_last_period = 0
            for n in Simulation.Households:
                if n.died_last_period == 1:
                    Settings.died_last_period += 1


class Simulation(Agent):

    # Static fields
    Households = Agent()
    houses_for_sale = []

    time = 1

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents
        # Children of simulation:
        Simulation.Banks = Agent(self)
        Simulation.Houses = Agent(self)
        self._statistics = Statistics(self)
        Simulation.Households = Agent(self)

        for _ in range(Settings.number_of_banks):
            Bank(Simulation.Banks)

        for _ in range(Settings.number_of_agents):
            Household(Simulation.Households)

        for _ in range(Settings.number_of_houses):
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
                self.event_proc(Event.period_end)
                Simulation.time += 1


            # Stop the simulation
            self.event_proc(Event.stop)  # 9

        if id_event == Event.period_start:  # 10
            # Adding new born persons to the population
            #lav evt. modellen mere stokastisk ved at føde et bestemt antal hver måned
            for _ in range(Settings.died_last_period):
                Household(Simulation.Households)
                print ("agent added, period: {}".format(Simulation.time))
            super().event_proc(id_event)

        else:
            # All other events are sent to decendants
            super().event_proc(id_event)
#We run the simulation
if Settings.random_seed != 0:
    random.seed(Settings.random_seed)
Simulation()
