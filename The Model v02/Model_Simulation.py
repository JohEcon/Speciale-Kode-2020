# We import the DREAM agent
import numpy
from Data import *
from Settings import *
from dream_agent import *

# We allocate an agent object

Model = Agent()

class Loan(Agent):
    def __init__(self, parent = None, principal = None, interest = None, annuity = None, owner = None):
        super().__init__(parent)
        self._principal = principal
        self._interest = interest
        self._annuity = annuity
        self._duration = Settings.loan_length * Settings.periods_in_year
        self._time_left = Settings.loan_length * Settings.periods_in_year
        self._periods = Settings.periods_in_year
        self._owner = owner


    def __repr__(self):
        return "Loan(ID: {a}, principal: {b}, interest: {c}, annuity: {d} duration: {e}, time left: {f}, owner: {g})".format(
            a = self.get_id(), b = round(self._principal), c = round(self._interest, 4), d = round(self._annuity), e = self._duration, f = self._time_left, g = self._owner.get_id())

    @property
    def principal(self):
        return self._principal

    @property
    def interest(self):
        return self._interest

    @property
    def annuity(self):
        return self._annuity

    @property
    def duration(self):
        return self._duration

    @property
    def time_left(self):
        return self._time_left

    @property
    def owner(self):
        return self._owner

    def interest_payment(self):
        int_payment = self._interest/Settings.periods_in_year * self._principal
        return int_payment

    def annuity_after_tax(self):
        after_tax = self.annuity - self.interest_payment() * Settings.interest_tax
        return after_tax

    def pay_annuity(self):
        self._principal += -self._annuity + self.interest_payment()
        self._time_left += -1
        if self._time_left == 0:
            #print("Loan {} paid in full in period {}".format(self.get_id(), Simulation.time))
            self.remove_this_agent()

    def event_proc(self, id_event):
        if id_event == Event.update:
            self.pay_annuity()

        if id_event == Event.stop:
            print(repr(self))


class Rent_unit(Agent):
    def __init__(self, parent = None, quality = 0.05, annuity = 2500):
        super().__init__(parent)
        self._parent = parent
        self._quality = quality
        self._annuity = annuity

    @property
    def quality(self):
        return self._quality

    @property
    def annuity(self):
        return self._annuity

class Houses(Agent):
    def __init__(self, parent = None, quality = 0, owner = None, price = 0, for_sale = True, seller = None):
        super().__init__(parent)
        self._parent = parent
        self._quality = quality
        self._owner = owner
        self._price = price
        self._for_sale = for_sale
        self._seller = seller
        self._periods_for_sale = 0

    def __repr__(self):
        return "House(ID: {a}, quality: {b}, price: {c}, owner: {d}, for sale: {e}, seller:{f}, periods for sale: {g})".format(
            a = self.get_id(), b = round(self._quality, 4), c = round(self._price), d = self.owner.get_id() if self.owner != None else None,
            e = self._for_sale, f = self.seller.get_id() if self.seller != None else None, g = self._periods_for_sale)

    @property
    def quality(self):
        return self._quality

    @property
    def for_sale(self):
        return self._for_sale

    @property
    def owner(self):
        return self._owner

    @property
    def price(self):
        return self._price

    @property
    def seller(self):
        return self._seller

    @property
    def periods_for_sale(self):
        return self._periods_for_sale

    def setting_owner(self, owner):
        self._owner = owner

    def setting_seller(self, seller):
        self._seller = seller

    def setting_for_sale(self, seller):
        if self._for_sale == False:
            self._for_sale = True
            self._seller = seller
            self._periods_for_sale = 0
            Simulation.houses_for_sale.append(self)
        else:
            pass

    def price_change(self, change_pct):
        self._price = self._price * (1 + change_pct)
        if self._price <0:
            self._price = 0

    def increase_periods_for_sale(self):
        self._periods_for_sale += 1

    def unlisting_house(self):
        self._periods_for_sale = 0
        self._for_sale = False
        Simulation.houses_for_sale.remove(self)

    def set_price(self, price):
        self._price = price
        #print("House {} price set to {}". format(self.get_id(), self._price))


    def event_proc(self, id_event):
        if id_event == Event.start:
            self._quality = random.uniform(0, 1)
            self._square_meters = random.uniform(50, 400)
            self._price = self._quality*2500000

        if id_event == Event.period_start:
            if self._for_sale == True:
                self.increase_periods_for_sale()

        if id_event == Event.update:
            if self._for_sale == True and self._owner == None and self._seller == None and self._periods_for_sale % Settings.price_adjustment_frequency == 0:
                self.price_change(-0.05)

        if id_event == Event.stop:
            print(repr(self))

class Bank(Agent):
    def __init__(self, parent = None, interest = Settings.interest):
        super().__init__(parent)
        self._interest = interest

        # Children of bank:
        Bank.Loans = Agent(self)

    @property
    def interest(self):
        return self._interest
    # Method that tells a household the price cap for house purchase given income and equity
    def max_budget_household(self, lender):
        piti = lender.income * Settings.piti_multiplier
        interest = Settings.interest
        max_loan = (piti*(1-(1 + interest/Settings.periods_in_year)**(-(Settings.loan_length*Settings.periods_in_year))))/(interest/Settings.periods_in_year)
        if lender.equity !=None:
            max_budget = max_loan + lender.equity
        else:
            max_budget = max_loan
        return max_budget

    def get_annuity(self, principal):
        interest = Settings.interest
        annuity = ( principal * (interest/Settings.periods_in_year) ) / ((1 - (1 + (interest / Settings.periods_in_year)) ** ( - (Settings.loan_length*Settings.periods_in_year) )))
        if annuity < 0:
            annuity = 0
        return annuity

    def get_loan(self, house, owner):
        if owner.equity != None:
            principal = house.price - owner.equity
        else:
            principal = house.price
        if principal < 0:
            owner._wealth += -principal

        if principal >= 0:
            annuity = self.get_annuity(principal)
            owner.set_loan(Loan(parent=Bank.Loans, principal=principal, interest=Settings.interest, annuity=annuity, owner=owner))

    def event_proc(self, id_event):
        super().event_proc(id_event)
        if id_event == Event.period_start:
            pass

class Household(Agent):

    def __init__(self, parent=None, wealth = 0, pdeath = 0, age = Settings.starting_age, house_owned = None, dead = False, moving = False, max_budget = 0):
        super().__init__(parent)
        self._wealth = wealth
        self._income = Settings.starting_income * (1 + numpy.random.normal(0, 0.1))
        self._age = age
        self._pdeath = pdeath
        self._dead = dead
        self._moving = moving
        self._house_owned = house_owned
        self._house_selling = None
        self._max_budget = max_budget
        self._houses_bought = 0
        self._loan = None
        self._equity = None
        self._utility_alpha = Settings.utility_alpha
        if self._loan != None:
            self._disposable = pay_income_taxes(self._income) - self._loan.annuity
        else:
            self._disposable = pay_income_taxes(self._income)

    def __repr__(self):
        return "Household(ID: {a}, Wealth: {b}, Income: {c}, after_tax: {aa}, disposable income: {cc}, Age: {d}, House ID: {e}, House quality: {f}, house selling: {ff}, utility: {dd}, p-death: {g}, max budget: {h}, loan id:{bb} moving: {i}, houses bought: {j}, alpha: {k} )".format(
            a = self._id, b=round(self._wealth),
            c = round(self._income), d=self._age,
            e = self._house_owned.get_id() if self.house_owned != None else None,
            f = round(self.house_owned.quality, 4) if self._house_owned != None else None,
            g = round(self._pdeath, 4), h=round(self._max_budget), i=self._moving, j=self._houses_bought,
            aa = round(pay_income_taxes(self._income)),
            k = round(self._utility_alpha, 3),
            bb = self._loan.get_id() if self._loan != None else None,
            cc = round(self._disposable),
            dd = round(self.household_utility(self.house_owned),1),
            ff = self._house_selling.get_id() if self._house_selling != None else None)

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

    @property
    def house_selling(self):
        return self._house_selling

    # Report Income
    @property
    def income(self):
        return self._income

    @property
    def equity(self):
        return self._equity

    # Report Age
    @property
    def age(self):
        return self._age

    #report if dead
    @property
    def dead(self):
        return self._dead

    @property
    def loan(self):
        return self._loan

    @property
    def utility_alpha(self):
        return self._utility_alpha


    def household_dies(self):
        Simulation.dead_this_period += 1
        self._dead = True
        # remove loan
        if self.loan != None:
            self.loan.remove_this_agent()
        # set house for sale
        if self.house_owned != None:
            self.house_owned.setting_for_sale(self)

    # We define hte household utility used for evaluating houses and for evaluating current house utility
    def household_utility(self, house):
        if house != self.house_owned:
            annuity = Simulation.bank.get_annuity(house.price - self.equity if self.equity != None else house.price)
        if house == self.house_owned:
            if self.loan != None:
                annuity = self.loan.annuity
            else:
                annuity = 0

        spending = pay_income_taxes(self.income) - annuity
        if self.house_owned != None:
            quality = house.quality
        else:
            quality = 0
        a = self.utility_alpha
        cd_utility = (spending ** a) * (1000 * quality) ** (1 - a)
        return cd_utility

    def set_loan(self, loan):
        self._loan = loan

    def communication(self, communicate, agent):
        if communicate == Communication.buy_house:

            #buy house and transfer funds to owner (if owner exists)
            self._wealth += -agent.price
            self._houses_bought += 1
            if agent.seller != None:
                agent.seller.communication(Communication.sell_house, agent)
            else:
                pass
            #Set you as owner of house
            self._house_owned = agent
            agent.setting_owner(self)
            #unlist house
            agent.unlisting_house()

        if communicate == Communication.sell_house:
            #get money form purchase
            self._wealth += agent.price
            #remove yourself as seller
            agent.setting_seller(None)
            self._house_selling = None
            #remove self as owner, if still owner
            if self.house_owned == agent:
                self._house_owned = None
            else:
                pass


    def event_proc(self, id_event):
        #checking if household is dead
        #initiating behaviour of living household
        if id_event == Event.start:
            pass

        if id_event == Event.period_start:
            if self._dead == True and self.house_owned == None:
                self.remove_this_agent()

            if self._house_owned != None:
                if self.loan != None:
                    self._equity = self.house_owned.price - self.loan.principal
                else:
                    self._equity = self.house_owned.price

            else:
                self._disposable = pay_income_taxes(self._income) - Simulation.rent_unit.annuity

        if id_event == Event.update:  # 2
            if self._dead == False:
                #set disposable income
                if self._loan != None:
                    self._disposable = pay_income_taxes(self._income) - self._loan.annuity
                else:
                    self._disposable = pay_income_taxes(self._income)

                #add income after tax to wealth
                self._wealth += pay_income_taxes(self._income)

                if self.house_selling != None:
                    if self.house_selling.periods_for_sale % Settings.price_adjustment_frequency == 0:
                        self.house_selling.price_change(Settings.price_adjustment)

            #check if household wants to move, if so, initiate moving procedure. Households wont move if they have not sold old house yet
                if random.uniform(0,1) < dict_move_prop[self.age] and self._moving == False and self._house_selling == None:
                    self._moving = True

                    #if already house owner, set own house for sale
                    if self._house_owned != None:
                        self._house_selling = self.house_owned
                        self.house_owned.setting_for_sale(self)
                    else:
                        pass

                if self._moving == True:
                    best_house = None
                    first = True
                    # Asking the bank how much the largest possible loan the household can get is (Budget constraint)
                    self._max_budget = Simulation.bank.max_budget_household(self)

                    # Agents find up to 4 houses they can afford
                    houses_checked = 0
                    houses_in_survey = []
                    while len(houses_in_survey) <= Settings.houses_surveyed and houses_checked < Settings.max_houses_checked:
                        if Simulation.houses_for_sale:
                            house_check = random.choice(Simulation.houses_for_sale)
                            houses_checked += 1
                            if house_check.price <= self._max_budget and houses_in_survey.count(house_check) < 1:
                                houses_in_survey.append(house_check)
                        if not Simulation.houses_for_sale:
                            break
                        #print(houses_in_survey)

                    #Agents find the best house out of the chosen ones
                    for n in houses_in_survey:
                        if n != self.house_owned and self != n.seller:
                            if first == True:
                                best_house = n
                                first = False
                            if self.household_utility(n) > self.household_utility(best_house):
                                best_house = n
                            else:
                                pass
                    if best_house == None:
                        pass

                    #buy the best house found:
                    if best_house != None:
                        #remove former loan
                        if self.loan != None:
                            self.loan.remove_this_agent()

                        # get loan for house
                        Simulation.bank.get_loan(best_house, self)

                        # buy the best house found
                        self.communication(Communication.buy_house, best_house)

                        self._moving = False
                    else:
                        pass

                #check if agent dies
                if random.uniform(0, 1) < self._pdeath:
                    self.household_dies()


        if id_event == Event.update_year:
            if self._dead == False:
                # every year, increase age by 1 and update income
                self._age += 1
                self._pdeath = prop_death(self._age)

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
                    self.household_dies()


        elif id_event == Event.stop:
            if self._dead == False:
                print(repr(self))

class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:
            Statistics.income = []
            Statistics.wealth = []

        if id_event == Event.period_end:
            Statistics.wealth = [h.wealth for h in Simulation.households]
            Statistics.income = [h.income for h in Simulation.households]

        if id_event == Event.stop:
            pass

class Simulation(Agent):
    # Static fields
    Households = Agent()
    time = 1
    bank = None
    rent_unit = None

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents
        # Children of simulation:
        Simulation.rent_unit = Rent_unit(self)
        Simulation.houses = Agent(self)
        self._statistics = Statistics(self)
        Simulation.bank = Bank(self)
        Simulation.households = Agent(self)

        for _ in range(Settings.number_of_agents):
            Household(Simulation.households)

        for _ in range(Settings.number_of_houses):
            Houses(Simulation.houses)

        # Start the simulation
        self.event_proc(Event.start)

    def event_proc(self, id_event):
        if id_event == Event.start:
            Simulation.houses_for_sale = []
            Simulation.outstanding_loans = []
            super().event_proc(id_event)
            # set houses for sale
            for n in Simulation.houses:
                Simulation.houses_for_sale.append(n)

            # The Event Pump
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.period_start)
                self.event_proc(Event.update)
                if Simulation.time % Settings.periods_in_year == 0:
                    self.event_proc(Event.update_year)
                self.event_proc(Event.period_end)
                Simulation.time += 1


            # Stop the simulation
            self.event_proc(Event.stop)

        if id_event == Event.period_start:
            #make counter for number of deaths this period
            Simulation.dead_this_period = 0
            super().event_proc(id_event)

        if id_event == Event.period_end:
            # Adding new born persons to the population
            for _ in range(Simulation.dead_this_period):
                    Household(Simulation.households)
                    print("agent added in {}".format(Simulation.time))
            super().event_proc(id_event)

        else:
            super().event_proc(id_event)
#We run the simulation

if Settings.random_seed != 0:
    numpy.random.seed(Settings.random_seed)

Simulation()




