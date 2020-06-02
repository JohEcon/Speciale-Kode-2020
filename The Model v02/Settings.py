

#We define the probability of death at a given age:
def prop_death(age):
    x = 0.0005 + 10 ** (-4.2 + 0.038 * age)
    return x

#we define the household utility function
def household_utility(income, a, b):
    x = income*a*b
    return x

#we define a method to find the agent with a given id
def get_agent_with_id(agent_type, agent_id):
    agent = None
    agent_found = False
    for n in agent_type:
        if agent_found == True:
            break
        if n.id() == agent_id:
            agent = n
            agent_found = True
        else:
            pass
    return agent

#we define a method to pay taxes on income
def pay_income_taxes(income):
    arb_bidrag = income * Settings.arbejdsmarkedsbidrag
    bundskat = 0
    topskat = 0

    if income >= Settings.bundfradrag/Settings.periods_in_year:
        bundskat = (income-Settings.bundfradrag/Settings.periods_in_year) * Settings.bundskat

    if income > Settings.topskat_limit/Settings.periods_in_year:
        topskat = (income - Settings.topskat_limit/Settings.periods_in_year) * Settings.topskat

    after_tax_income = income - arb_bidrag - bundskat - topskat
    skattetryk = (1 - after_tax_income / income)

    if (1 - skattetryk) < (1 - (Settings.skatteloft + Settings.arbejdsmarkedsbidrag)):
        after_tax_income = income * (1 - (Settings.skatteloft + Settings.arbejdsmarkedsbidrag))

    return after_tax_income

class Settings: pass
#Number of agents and periods settings
Settings.number_of_agents = 10
Settings.number_of_banks = 1
Settings.number_of_houses = 10
Settings.number_of_periods = 1000
Settings.periods_in_year = 12

#tax settings
Settings.bundfradrag = 46500
Settings.topskat_limit = 531000 * 1.08
Settings.arbejdsmarkedsbidrag = 0.08
Settings.bundskat = 0.26 + 0.0075 + 0.1211
Settings.topskat = 0.15
Settings.skatteloft = 0.5206

#income and age settings
Settings.starting_income = 10000
Settings.su_income = 6200
Settings.kh_income = 11500
Settings.pension_share = 0.8
Settings.starting_age = 20
Settings.retire_age = 67
Settings.max_age = 109
deaths_period = []

#Bank and loan settings
Settings.starting_interest = 0.01
Settings.piti_multiplier = 0.28
Settings.interest = 0.04
Settings.loan_lenght = 30

#other settings
Settings.out_file = "Statistics.py"
Settings.graphics_show = False
Settings.graphics_periods_per_pic = 12


# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.period_start = 3 #
Event.update = 4 # Agent behavior
Event.period_end = 5 #consolidation of what happened last period
Event.update_year = 6 #Agent behavior which only happends once a year

class Communication: pass
Communication.buy_house = 1
Communication.sell_house = 2
