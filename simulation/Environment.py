import numpy as np
from random import uniform
from simulation.Vector import *
from simulation.State import State
from simulation.Action import Action

class Environment:
    def __init__(self, agents, epsilon, learning_rate, discount_factor, obstacle_position, obstacle_radius, separation_magnitude, cohesion_magnitude, alignment_magnitude, max_speed, max_length, width, height, inner_sensor, outer_sensor, agent_size):
        self.action_class = Action(agents, max_speed, max_length, separation_magnitude, alignment_magnitude, cohesion_magnitude)
        self.state_class = State(width, height, inner_sensor, outer_sensor, agent_size, obstacle_position, obstacle_radius)
        self.agents = agents
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.separation_magnitude = separation_magnitude
        self.cohesion_magnitude = cohesion_magnitude
        self.alignment_magnitude = alignment_magnitude
        self.states  = ['Crash',
                        'Close',
                        'Nearby',
                        'Alone',
                        'Lost ']
        self.actions = ['Separation',
                        'Alignment',
                        'Cohesion',
                        'Separation-Alignment',
                        'Separation-Cohesion',
                        'Alignment-Cohesion',
                        'Separation-Alignment-Cohesion']

    def create_Q_matrix(self, n_state=5):
        self.Q_values = []
        for i in range(0, n_state * 7, 7):
            row = []
            for j in range(i, i + 7, 1):
                row.append(float(uniform(-2,2)))
            self.Q_values.append(row)
        self.Q_values = np.array(self.Q_values ,dtype=float).reshape(n_state, 7)

    def update_state(self, self_agent, position):
        self.state = self.state_class.get_current_state(self_agent, self.agents, position)

    def update_next_state(self, self_agent, position):
        self.next_state, self.reward = self.state_class.get_next_state(self_agent, self.agents, position)

    def get_action(self):
        if np.random.random() > self.epsilon:
            self.action = np.argmax(self.Q_values[self.state])
            self.mode = 'Exploitation'
        else:
            self.action = np.random.randint(7)
            self.mode = 'Exploration'

    def update_action(self, self_agent, position, velocity):
        steering = Vector()

        if self.actions[self.action] == 'Separation' and self.state == 0:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
        elif self.actions[self.action] == 'Separation' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
        elif self.actions[self.action] == 'Separation' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
        elif self.actions[self.action] == 'Separation' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
        elif self.actions[self.action] == 'Separation' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
        elif self.actions[self.action] == 'Alignment' and self.state == 0:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 1:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 2:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 3:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 4:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Cohesion' and self.state == 0:
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Cohesion' and self.state == 1:
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Cohesion' and self.state == 2:
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Cohesion' and self.state == 3:
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Cohesion' and self.state == 4:
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 0:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Cohesion' and self.state == 0:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Cohesion' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Cohesion' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Cohesion' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Cohesion' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 0:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 1:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 2:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 3:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 4:
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 0:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        
        return steering

    def update_Q_matrix(self):
        old_q_value = self.Q_values[self.state][self.action]
        temporal_difference = self.reward + (self.discount_factor * np.max(self.Q_values[self.next_state])) - old_q_value
        new_q_value = old_q_value + (self.learning_rate * temporal_difference)
        self.Q_values[self.state][self.action] = new_q_value
        return self.Q_values