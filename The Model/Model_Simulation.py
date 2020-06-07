# We import the DREAM agent
from Houses import *
from Statistics import *
from Household import *
# We allocate an agent object
Model = Agent()

class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:                     #1
            self._file = open(Settings.out_file, "w")
            self._file.write("dict_deaths_period={}")
        elif id_event == Event.stop:                    #2
            self._file.close()

        elif id_event == Event.period_start:            #3
            for n in Simulation.Households:
                if n.died_this_period == 1:
                    print("Death of agent ID: {}, age: {}, dead: {}, period: {}".format(n._id, n._age, n._dead, Simulation.time-1))
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
                print("agent added - Period: {}".format(Simulation.time))

        else:
            # All other events are sent to decendants
            super().event_proc(id_event)

#We run the simulation
Simulation()
