# We import the DREAM agent
from dream_agent import Agent
# We define the Traders object
from mesa import Agent, Model


class HousingAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        # The agent's step will go here.
        pass

class HousingModel(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()


# We define the Statistics object




# We add our new objects to the model:
Model.add_agent(Statistics())
Model.add_agent(LOB())
Model.add_agent(Traders())

# We add agents to our Traders



#we print the total number of agents in our model
print(Model.get_total_number_of_agents())


class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.update = 3        # Agent behavior

