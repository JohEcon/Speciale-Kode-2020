

#We define the probability of death at a given age:
def prop_death(age):
    x = 0.0005 + 10 ** (-4.2 + 0.038 * age)
    return x

class Settings: pass
Settings.number_of_agents=10
Settings.number_of_periods=2000
Settings.periods_in_year=12
Settings.starting_income=10000
Settings.su_income=6200
Settings.kh_income=11500
Settings.starting_age= 20
Settings.retire_age=67
Settings.out_file="Statistics.py"
Settings.graphics_show = False
Settings.graphics_periods_per_pic = 12
Settings.number_of_houses = 10
Settings.starting_interest = 0.01
Settings.piti_multiplier = 0.28
Settings.number_of_banks = 4
Settings.interest = 0.04
Settings.loan_lenght = 1
deaths_period = []


# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.period_start = 3 #consolidation of what happened last period
Event.update = 4  # Agent behavior
Event.update_year = 5 #Agent behavior which only happends once a year