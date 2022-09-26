import numpy as np
from simulation.Vector import *
from simulation.Sensor import Sensor
from simulation.Behavior import Behavior
from implementation.VirtualEnvironment import VirtualEnvironment

class testAgent:
    def __init__(self, arena, agents, matrix_file, num_x, width, height, agent_name, target_x, target_y, start_x, start_y, inner, outer, max_speed, max_length, starting_angle, obstacle_position, obstacle_radius, text_font, agent_text_size, agent_color, agent_size, epsilon, learning_rate, discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude):
        self.arena = arena
        self.inner = inner
        self.outer = outer
        self.agent_name = agent_name
        self.num_x = num_x
        self.data_x = np.zeros(num_x)
        self.data_y = 0
        self.sum_error = 0

        self.target_position = Vector(target_x, target_y)
        self.position = Vector(start_x, start_y)
        self.velocity = Vector()
        self.acceleration = Vector()

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
        if dist >= 0 and dist <= 10:
            self.finish = True

    def update_acceleration(self, self_agent, agents, wander, avoid, target):
        self.acceleration.reset()
        self.acceleration += self.behavior.update_behavior(self.position, self.velocity, self.obstacle_position, wander, avoid, target)
        self.acceleration += self.environment.update_action(self_agent, self.position, self.velocity)
        self.crashing(agents)
        self.arriving()

    def dynamic(self, speed_set_point, Kp, Ki, a0, a1, b1, dt):
        x_k_min2 = self.data_x[self.num_x-1]
        x_k_min1 = self.data_x[self.num_x-2]
        y_k_pos1 = self.data_y
        y_k = a0 * x_k_min2 + a1 * x_k_min1 + b1 * y_k_pos1
        error = speed_set_point - y_k

        self.sum_error += error * dt
        x_k = Kp * error + Ki * self.sum_error
        if x_k < 0:
            x_k = 0
        if x_k > 100/255:
            x_k = 100/255
        
        self.data_x = np.delete(self.data_x, -1)
        self.data_x = np.insert(self.data_x, 0, x_k)
        self.data_y = y_k
        return y_k, x_k

    def update_kinematics(self, Kp, Ki, a0, a1, b1, dt):
        if self.crash is False and self.finish is False:
            speed_set_point = self.acceleration.magnitude() * 0.3683 * 0.01
            speed_out, mv = self.dynamic(speed_set_point, Kp, Ki, a0, a1, b1, dt)
            max_heading = 188.7 * dt
            acc_heading = self.acceleration.heading() * 180 / np.pi
            vel_heading = self.velocity.heading() * 180 / np.pi

            if vel_heading >= 0:
                if acc_heading >= 0:
                    if acc_heading < vel_heading and (vel_heading - acc_heading) > max_heading:
                        vel_heading = vel_heading - max_heading
                    elif acc_heading > vel_heading and (acc_heading - vel_heading) > max_heading:
                        vel_heading = vel_heading + max_heading
                    else:
                        vel_heading = acc_heading
                elif acc_heading < 0:
                    if (vel_heading - acc_heading) > max_heading:
                        vel_heading = vel_heading - max_heading
                    else:
                        vel_heading = acc_heading
            elif vel_heading < 0:
                if acc_heading <= 0:
                    if acc_heading < vel_heading and (vel_heading - acc_heading) > max_heading:
                        vel_heading = vel_heading - max_heading
                    elif acc_heading > vel_heading and (acc_heading - vel_heading) > max_heading:
                        vel_heading = vel_heading + max_heading
                    else:
                        vel_heading = acc_heading
                elif acc_heading > 0:
                    if (abs(vel_heading) + acc_heading) > max_heading:
                        vel_heading = vel_heading + max_heading
                    else:
                        vel_heading = acc_heading

            print(f"{self.agent_name} -> SP : {speed_set_point:.4f}\t PV : {speed_out:.4f}\t MV : {int(mv*255)}\t heading : {int(vel_heading)}")
            vel_x, vel_y = pol2cart(speed_out, vel_heading * np.pi / 180)
            self.velocity = Vector(vel_x, vel_y) / 0.3683 / 0.01
            self.position += self.velocity * dt
            self.angle = self.velocity.heading() + np.pi/2

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
                    if dist >= 2 * self.sensor.agent_size and dist <= self.outer + self.sensor.agent_size:
                        total += 1

        if total == len(agents)-2:
            return 1
        else:
            return 0