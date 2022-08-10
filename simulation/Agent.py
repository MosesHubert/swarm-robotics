import numpy as np
from random import uniform
from simulation.Vector import *
from simulation.Sensor import Sensor
from simulation.Behavior import Behavior
from simulation.Environment import Environment

class Agent:
    def __init__(self, arena, agents, width, height, agent_name, target_x, target_y, inner, outer, max_speed, max_length, starting_angle, obstacle_radius, text_font, agent_text_size, agent_color, agent_size, epsilon, learning_rate, discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude):
        self.arena = arena
        self.inner = inner
        self.outer = outer
        self.agent_name = agent_name

        self.target_position = Vector(target_x, target_y)
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()

        self.angle = starting_angle
        self.max_speed = max_speed
        self.max_length = max_length

        self.sensor = Sensor(self.arena, self.agent_name, inner, outer, text_font, agent_text_size, agent_color, agent_size, self.angle)
        self.behavior = Behavior(self.target_position, width, height, max_speed, max_length, self.inner, self.outer, obstacle_radius)
        self.environment = Environment(agents, epsilon, learning_rate, discount_factor, separation_magnitude, cohesion_magnitude, alignment_magnitude, max_speed, max_length, width, height, inner, outer, agent_size)
        self.environment.create_Q_matrix()

    def reset(self, start_x, start_y):
        self.crash = False
        self.finish = False
        self.position = Vector(start_x, start_y)
        vec_x = uniform(-1, 1)
        vec_y = uniform(-1, 1)
        self.velocity = Vector(vec_x, vec_y)
        self.velocity.normalize()
        self.velocity = self.velocity * uniform(1, 3)

    def get_first_state_action(self, self_agent):
        self.environment.update_state(self_agent, self.position)
        self.environment.get_action()
        self.state = self.environment.state
        self.action = self.environment.action
        self.mode = self.environment.mode

    def get_current_state(self, self_agent):
        self.environment.update_state(self_agent, self.position)
        self.state = self.environment.state

    def get_next_state(self, self_agent):
        self.environment.update_next_state(self_agent, self.position)
        self.next_state = self.environment.next_state

    def get_next_action(self):
        if self.state != self.next_state:
            self.environment.get_action()
            self.action = self.environment.action
            self.mode = self.environment.mode

    def crashing(self, agents):
        for agent in agents:
            dist = getDistance(self.position, agent.position)
            if agent is not self and dist <= 2 * self.sensor.agent_size:
                self.crash = True

    def arriving(self):
        dist = getDistance(self.position, self.target_position)
        if dist >= 0 and dist <= 1:
            self.finish = True

    def update_acceleration(self, self_agent, agents, obstacle_position, wander, avoid, target):
        self.acceleration.reset()
        self.acceleration += self.behavior.update_behavior(self.position, self.velocity, obstacle_position, wander, avoid, target)
        self.acceleration += self.environment.update_action(self_agent, self.position, self.velocity)
        self.crashing(agents)
        self.arriving()

    def update_kinematics(self):
        if self.crash is False and self.finish is False:
            self.position += self.velocity
            self.velocity += self.acceleration
            self.velocity.limit(self.max_speed)
            self.angle = self.velocity.heading() + np.pi/2

    def update_matrix_values(self, episode, track_version, obstacle_version):
        if self.state != self.next_state:
            q_matrix = self.environment.update_Q_matrix()
            np.savetxt('q_matrix/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}'.format(track_version, obstacle_version) + ".csv", q_matrix, delimiter=",")
            print(self.agent_name + ' (Episode {}) => State: '.format(episode+1) + self.environment.states[self.next_state] + ',\tMode: ' + self.mode + ',\tAction: ' + self.environment.actions[self.action])

    def draw_agent(self, inner_color, outer_color, head_color, state_color, action_color, mode_color):
        self.sensor.draw_sensor(self.position, self.environment.states[self.next_state], self.environment.actions[self.action], self.mode, inner_color, outer_color, head_color, state_color, action_color, mode_color, self.angle)

    def show_output(self, episode):
        print(self.agent_name + ' (Episode {}) => State: '.format(episode+1) + self.environment.states[self.state] + ',\tMode: ' + self.mode + ',\tAction: ' + self.environment.actions[self.action])

    def is_terminal_state(self, agents):
        total = 0
        target_dist = getDistance(self.position, self.target_position)

        if target_dist <= self.inner:
            for agent in agents:
                dist = getDistance(self.position, agent.position)
                if agent is not self:
                    if dist >= self.inner and dist <= self.outer:
                        total += 1

        if total == len(agents)-1:
            return 1
        else:
            return 0