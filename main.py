from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

class DominanceAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dominance = random.uniform(0, 1)

    def step(self):
        other_agent = random.choice(self.model.schedule.agents)
        if other_agent != self:
            self.interact(other_agent)

    def interact(self, other_agent):
        if self.dominance > other_agent.dominance:
            self.dominance += 0.01
            other_agent.dominance -= 0.01
        else:
            self.dominance -= 0.01
            other_agent.dominance += 0.01

class DominanceModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = DominanceAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Dominance": "dominance"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Run the model
model = DominanceModel(10, 10, 10)
for i in range(100):
    model.step()

# Collect and print the data
import pandas as pd

data = model.datacollector.get_agent_vars_dataframe()
print(data)
