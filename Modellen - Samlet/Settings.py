class Settings: pass
Settings.number_of_agents=100
Settings.number_of_periods=2000
Settings.periods_in_year=12
Settings.starting_income=10000
Settings.starting_age= 20
Settings.retire_age=67
Settings.statistics_file= "statistics.txt"
Settings.graphics_show = False
Settings.graphics_periods_per_pic = 12

# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.period_start = 3
Event.update = 4  # Agent behavior