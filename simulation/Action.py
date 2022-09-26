from simulation.Vector import *

class Action:
    def __init__(self, agents, outer, max_speed, max_length, separation_magnitude, alignment_magnitude, cohesion_magnitude):
        self.agents = agents
        self.outer = outer
        self.max_speed = max_speed
        self.max_length = max_length
        self.separation_magnitude = separation_magnitude
        self.alignment_magnitude = alignment_magnitude
        self.cohesion_magnitude = cohesion_magnitude

    def separation(self, self_agent, position, velocity):
        steering = Vector()

        for agent in self.agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist <= self.outer:
                vn = SubVectors(position, agent.position)
                vn.normalize()
                vn = vn / dist
                steering.add(vn)

        steering = steering * self.max_speed
        steering.limit(self.max_length)

        return steering

    def get_separation(self, self_agent, position, velocity):
        avoid = self.separation(self_agent, position, velocity)
        avoid = avoid * self.separation_magnitude
        return avoid

    def alignment(self, self_agent, position, velocity):
        total = 0
        steering = Vector()

        for agent in self.agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist <= self.outer:
                vn = agent.velocity
                steering.add(vn)
                total += 1
        if total > 0:
            steering = steering / total
            steering = steering * self.max_speed
            steering.limit(self.max_length)

        return steering

    def get_alignment(self, self_agent, position, velocity):
        align = self.alignment(self_agent, position, velocity)
        align = align * self.alignment_magnitude
        return align

    def cohesion(self, self_agent, position, velocity):
        total = 0
        steering = Vector()

        for agent in self.agents:
            dist = getDistance(position, agent.position)
            if agent is not self_agent and dist <= self.outer:
                vn = agent.position
                steering.add(vn)
                total += 1

        if total > 0:
            steering = steering / total
            steering = steering * self.max_speed
            steering.limit(self.max_length)

        return steering

    def get_cohesion(self, self_agent, position, velocity):
        gather = self.cohesion(self_agent, position, velocity)
        gather = gather * self.cohesion_magnitude
        return gather