import numpy as np
from simulation.Vector import *
from simulation.State import State
from simulation.Action import Action

class VirtualEnvironment:
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

    def import_Q_matrix(self, matrix_file):
        self.Q_values = np.genfromtxt('q_matrix/agent_{}.csv'.format(matrix_file), delimiter=',')

    def update_state(self, self_agent, position):
        self.state = self.state_class.get_current_state(self_agent, self.agents, position)

    def update_next_state(self, self_agent, position):
        self.next_state, self.reward = self.state_class.get_next_state(self_agent, self.agents, position)

    def get_action(self):
        self.action = np.argmax(self.Q_values[self.state])
        self.mode = ''

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
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 1:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 2:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 3:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Alignment' and self.state == 4:
            align = self.action_class.get_alignment(self_agent, position, velocity)
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
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
        elif self.actions[self.action] == 'Separation-Alignment' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
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
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 1:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 2:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 3:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Alignment-Cohesion' and self.state == 4:
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 0:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 1:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 2:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 3:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        elif self.actions[self.action] == 'Separation-Alignment-Cohesion' and self.state == 4:
            avoid = self.action_class.get_separation(self_agent, position, velocity)
            steering.add(avoid)
            align = self.action_class.get_alignment(self_agent, position, velocity)
            steering.add(align)
            gather = self.action_class.get_cohesion(self_agent, position, velocity)
            steering.add(gather)
        
        return steering