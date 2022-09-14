import numpy as np
from random import uniform
from simulation.Vector import *
from simulation.Sensor import Sensor
from simulation.Behavior import Behavior
from implementation.BB8_move import Move
from implementation.VirtualEnvironment import VirtualEnvironment

class VirtualAgent:
    def __init__(self, arena, agent, agents, matrix_file, width, height, agent_name, target_x, target_y, inner, outer, max_speed, max_length, starting_angle, obstacle_position, obstacle_radius, text_font, agent_text_size, agent_color, agent_size, epsilon, learning_rate, discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude):
        self.arena = arena
        self.inner = inner
        self.outer = outer
        self.agent = Move(agent)
        self.agent_name = agent_name
        self.sum_error = 0

        self.target_position = Vector(target_x, target_y)
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        self.virtual_position = Vector()

        self.angle = starting_angle
        self.max_speed = max_speed
        self.max_length = max_length
        self.obstacle_position = obstacle_position
        self.obstacle_radius = obstacle_radius

        self.sensor = Sensor(self.arena, self.agent_name, inner, outer, text_font, agent_text_size, agent_color, agent_size, self.angle)
        self.behavior = Behavior(self.target_position, width, height, max_speed, max_length, self.inner, self.outer, obstacle_radius)
        self.environment = VirtualEnvironment(agents, epsilon, learning_rate, discount_factor, obstacle_position, obstacle_radius, separation_magnitude, cohesion_magnitude, alignment_magnitude, max_speed, max_length, width, height, inner, outer, agent_size)
        self.environment.import_Q_matrix(matrix_file)

    def reset(self):
        self.crash = False
        self.finish = False
        self.sum_error = 0

    def get_position(self, cx, cy):
        self.position = Vector(cx, cy)

    def get_first_state_action(self, self_agent):
        self.environment.update_state(self_agent, self.position)
        self.environment.get_action()
        self.state = self.environment.state
        self.action = self.environment.action
        self.mode = self.environment.mode

    def get_current_state(self, self_agent):
        self.environment.update_state(self_agent, self.position)
        self.state = self.environment.state
        # print(f'{self.agent_name} > State: {self.state}')

    def get_next_state(self, self_agent):
        self.environment.update_next_state(self_agent, self.position)
        self.next_state = self.environment.next_state
        # print(f'{self.agent_name} > Next State: {self.next_state}')

    def get_next_action(self):
        if self.state != self.next_state:
            self.environment.get_action()
            self.action = self.environment.action
            self.mode = self.environment.mode
            print(self.agent_name + ' => State: ' + self.environment.states[self.next_state] + ',\tAction: ' + self.environment.actions[self.action])

    def crashing(self, agents):
        obstacle = Vector(self.obstacle_position[0], self.obstacle_position[1])
        obstacle_dist = getDistance(self.position, obstacle)
        for agent in agents:
            dist = getDistance(self.position, agent.position)
            if agent is not self and dist <= 2 * self.sensor.agent_size:
                self.crash = True
        if obstacle_dist <= self.sensor.agent_size + self.obstacle_radius:
            self.crash = True

    def arriving(self):
        dist = getDistance(self.position, self.target_position)
        if dist >= 0 and dist <= 5:
            self.finish = True

    def update_acceleration(self, self_agent, agents, wander, avoid, target):
        self.acceleration.reset()
        self.acceleration += self.behavior.update_behavior(self.position, self.velocity, self.obstacle_position, wander, avoid, target)
        self.acceleration += self.environment.update_action(self_agent, self.position, self.velocity)
        self.crashing(agents)
        self.arriving()

    def control(self, velocity_set_point, Kp, Ki, real_velocity, dt):
        error = velocity_set_point - real_velocity
        self.sum_error += error * dt
        output = Kp * error + Ki * self.sum_error
        output = output * 255
        return output

    def update_kinematics(self, real_velocity, Kp, Ki, dt):
        if self.crash is False and self.finish is False:
            self.velocity += self.acceleration
            self.angle = self.velocity.heading() + np.pi/2
            speed_set_point = self.velocity.magnitude() * 0.3683 * 0.01
            speed_out = int(self.control(speed_set_point, Kp, Ki, real_velocity, dt))
            heading = int(self.velocity.heading() / np.pi * 180)

            if heading < 0:
                if self.velocity.y < 0:
                    heading = 360 + heading
                elif self.velocity.x < 0:
                    heading = -1 * heading
                    heading = 90 + heading
            elif heading > 0:
                if self.velocity.y < 0 and self.velocity.x < 0:
                    heading = 180 + heading

            if speed_out < 0:
                speed_out = int(-1 * speed_out)
            
            if speed_out > 100:
                speed_out = int(100)
            
            self.agent.drive(speed_out, heading, dt)
            # print(f"{self.agent_name} -> SP : {speed_set_point:.4f}\t PV : {real_velocity:.4f}\t MV : {speed_out}\t heading : {heading}")
            vel_x, vel_y = pol2cart(speed_out, self.velocity.heading())
            self.velocity = Vector(vel_x, vel_y)
        else:
            self.agent.drive(0, 0, dt)

    def draw_agent(self, inner_color, outer_color, head_color, state_color, action_color, mode_color):
        self.sensor.draw_sensor(self.position, self.environment.states[self.next_state], self.environment.actions[self.action], self.mode, inner_color, outer_color, head_color, state_color, action_color, mode_color, self.angle)

    def show_output(self):
        print(self.agent_name + ' => State: ' + self.environment.states[self.state] + ',\tAction: ' + self.environment.actions[self.action])

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