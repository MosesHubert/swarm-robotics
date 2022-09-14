from simulation.Vector import *

class State:
    def __init__(self, width, height, inner_sensor, outer_sensor, agent_size, obstacle_position, obstacle_radius):
        self.width = width
        self.height = height
        self.inner_sensor = inner_sensor
        self.outer_sensor = outer_sensor
        self.agent_size = agent_size
        self.obstacle_position = Vector(obstacle_position[0], obstacle_position[1])
        self.obstacle_radius = obstacle_radius

    def crash(self, self_agent, agents, position):
        total = 0
        obstacle_dist = getDistance(position, self.obstacle_position)

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist <= 2 * self.agent_size:
                total += 1
        if obstacle_dist <= self.agent_size + self.obstacle_radius:
            total += 1

        if total > 0:
            self.state = 0

    def next_crash(self, self_agent, agents, position):
        total = 0
        obstacle_dist = getDistance(position, self.obstacle_position)

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist <= 2 * self.agent_size:
                total += 1
        if obstacle_dist <= self.agent_size + self.obstacle_radius:
            total += 1

        if total > 0:
            self.next_state = 0
            self.reward = -1

    def close(self, self_agent, agents, position):
        total = 0

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent:
                if dist > 2 * self.agent_size and dist < self.inner_sensor:
                    total += 1
        
        if total > 0:
            self.state = 1

    def next_close(self, self_agent, agents, position):
        total = 0

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent:
                if dist > 2 * self.agent_size and dist < self.inner_sensor:
                    total += 1
        
        if total > 0:
            self.next_state = 1
            self.reward = 0

    def nearby(self, self_agent, agents, position):
        total = 0

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent:
                if dist >= self.inner_sensor and dist <= self.outer_sensor:
                    total += 1

        if total > 0:
            self.state = 2

    def next_nearby(self, self_agent, agents, position):
        total = 0

        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent:
                if dist >= self.inner_sensor and dist <= self.outer_sensor:
                    total += 1

        if total > 0:
            self.next_state = 2
            self.reward = 1

    def alone(self, self_agent, agents, position):
        total = 0
        
        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist > self.outer_sensor:
                total += 1
        
        if total == len(agents)-1:
            self.state = 3

    def next_alone(self, self_agent, agents, position):
        total = 0
        
        for agent in agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist > self.outer_sensor:
                total += 1
        
        if total == len(agents)-1:
            self.next_state = 3
            self.reward = 0

    def lost(self, position):
        total = 0

        if position.x >= self.width or position.x <= 0:
            total += 1
        if position.y >= self.height or position.y <= 0:
            total += 1

        if total > 0:
            self.state = 4

    def next_lost(self, position):
        total = 0

        if position.x >= self.width or position.x <= 0:
            total += 1
        if position.y >= self.height or position.y <= 0:
            total += 1

        if total > 0:
            self.next_state = 4
            self.reward = -1

    def get_current_state(self, self_agent, agents, position):
        self.alone(self_agent, agents, position)
        self.lost(position)
        self.nearby(self_agent, agents, position)
        self.close(self_agent, agents, position)
        self.crash(self_agent, agents, position)
        return self.state

    def get_next_state(self, self_agent, agents, position):
        self.next_alone(self_agent, agents, position)
        self.next_lost(position)
        self.next_nearby(self_agent, agents, position)
        self.next_close(self_agent, agents, position)
        self.next_crash(self_agent, agents, position)
        return self.next_state, self.reward