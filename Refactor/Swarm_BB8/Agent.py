from re import A
import numpy as np
from Swarm_BB8 import Vector
from Swarm_BB8 import Sensor
from Swarm_BB8 import Dynamics

class Agent:
    number_of_agents = 0

    def __init__(self,mode="sim"):
        Agent.number_of_agents += 1
        self.id = Agent.number_of_agents
        if mode == "sim":
            self.dynamic =  Dynamics.Sim_BB8
        elif mode == "real":
            self.dynamic = Dynamics.Real_BB8
        self.position = Vector()
        self.velocity = Vector()
        self.sensor = Sensor(self.position)

    def get_position(self):
        return self.position

    def get_nearby(self,agents):
        ids = self.sensor.get_nearby_agent(self,agents)
        return ids
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return f'agent-{self.id}'