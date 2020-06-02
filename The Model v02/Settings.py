

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

"""def get_agent_with_method(agent_type, agent_id, method):
    agent_found = False
    agent = None
    command = method
    for n in agent_type:
        if agent_found == True:
            break
        if n.get_id() == agent_id:
            agent = n
            agent_found = True
        else:
            pass
    agent_command = "agent.command()"
    if agent != None and command != None:
        return agent_command
    if agent != None and command == None:
        return agent
    else:
        return agent"""

class Settings: pass
#Number of agents and periods settings
Settings.number_of_agents = 10
Settings.number_of_banks = 1
Settings.number_of_houses = 10
Settings.number_of_periods = 1000
Settings.periods_in_year = 12

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
Event.period_start = 3 #consolidation of what happened last period
Event.update = 4  # Agent behavior
Event.update_year = 5 #Agent behavior which only happends once a year

class Communication: pass
Communication.buy_house = 1
Communication.sell_house = 2
