# We import the DREAM agent
from dream_agent import Agent

# We allocate an agent object
Model = Agent()

# We define the Traders object
class Traders(Agent):
    def __init__(self, parent=None, ID="", Endow=0):
        super().__init__(parent)
        self._ID = ID
        self._Endow = Endow

# We define the Statistics object

# We add our new objects to the model:
Model.add_agent(Statistics())
Model.add_agent(LOB())
Model.add_agent(Traders())

# We add agents to our Traders
market_maker=Traders()
market_maker(parent=Traders, ID=1, Endow=10)



#we print the total number of agents in our model
print(Model.get_total_number_of_agents())


class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.update = 3        # Agent behavior

segsesesegewssegseg