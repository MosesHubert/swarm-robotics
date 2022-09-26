import numpy as np
import pandas as pd
from simulation.Vector import *
from simulation.Sensor import Sensor
from simulation.Behavior import Behavior
from simulation.Environment import Environment

class Agent:
    def __init__(self, arena, agents, num_x, width, height, agent_name, target_x, target_y, inner, outer, max_speed, max_length, starting_angle, obstacle_position, obstacle_radius, text_font, agent_text_size, agent_color, agent_size, epsilon, learning_rate, discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude):
        self.arena = arena
        self.inner = inner
        self.outer = outer
        self.agent_name = agent_name
        self.num_x = num_x
        self.data_x = np.zeros(num_x)
        self.data_y = 0 # np.zeros(2)
        self.sum_error = 0

        self.target_position = Vector(target_x, target_y)
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()

        self.angle = starting_angle
        self.max_speed = max_speed
        self.max_length = max_length
        self.obstacle_position = obstacle_position
        self.obstacle_radius = obstacle_radius

        self.sensor = Sensor(self.arena, self.agent_name, inner, outer, text_font, agent_text_size, agent_color, agent_size, self.angle)
        self.behavior = Behavior(self.target_position, width, height, max_speed, max_length, self.inner, self.outer, obstacle_radius)
        self.environment = Environment(agents, epsilon, learning_rate, discount_factor, obstacle_position, obstacle_radius, separation_magnitude, cohesion_magnitude, alignment_magnitude, max_speed, max_length, width, height, inner, outer, agent_size)
        self.environment.create_Q_matrix()

    def reset(self, start_x, start_y):
        self.crash = False
        self.finish = False
        self.clamped = False
        self.position = Vector(start_x, start_y)
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

    def get_next_state(self, self_agent):
        self.environment.update_next_state(self_agent, self.position)
        self.next_state = self.environment.next_state

    def get_next_action(self):
        if self.state != self.next_state:
            self.environment.get_action()
            self.action = self.environment.action
            self.mode = self.environment.mode

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
        if dist >= 0 and dist <= 10: # 13.5
            self.finish = True

    def update_acceleration(self, self_agent, agents, wander, avoid, target):
        self.crashing(agents)
        self.arriving()
        if self.crash is False and self.finish is False:
            self.acceleration.reset()
            self.acceleration += self.behavior.update_behavior(self.position, self.velocity, self.obstacle_position, wander, avoid, target)
            self.acceleration += self.environment.update_action(self_agent, self.position, self.velocity)
        else:
            self.acceleration.reset()

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

        # if not self.clamped:
        #     x_k1 = Kp * error + Ki * self.sum_error
        # elif self.clamped:
        #     x_k1 = Kp * error
        
        # if x_k1 < 0:
        #     x_k2 = 0 
        # if x_k1 > 100/255:
        #     x_k2 = 100/255
        # if x_k1 >= 0 and x_k1 <= 100/255:
        #     x_k2 = x_k1
        
        # if x_k1 < 0 and error < 0:
        #     if x_k1 != x_k2:
        #         self.clamped = True
        # elif x_k1 > 0 and error > 0:
        #     if x_k1 != x_k2:
        #         self.clamped = True
        # else:
        #     self.clamped = False

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

            print(f"{self.agent_name} -> SP : {speed_set_point:.4f}\t PV : {speed_out:.4f}\t MV : {int(mv*255)}\t heading : {vel_heading:.4f}")
            vel_x, vel_y = pol2cart(speed_out, vel_heading * np.pi / 180)
            self.velocity = Vector(vel_x, vel_y) / 0.3683 / 0.01
            self.position += self.velocity * dt
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
                    if dist >= 2 * self.sensor.agent_size and dist <= self.outer + self.sensor.agent_size:
                        total += 1

        if total == len(agents)-2:
            return 1
        else:
            return 0

    def df_Q_values(self):
        self.Q_crash = pd.DataFrame(self.environment.Q_values[0]).transpose()
        self.Q_close = pd.DataFrame(self.environment.Q_values[1]).transpose()
        self.Q_nearby = pd.DataFrame(self.environment.Q_values[2]).transpose()
        self.Q_alone = pd.DataFrame(self.environment.Q_values[3]).transpose()
        self.Q_lost = pd.DataFrame(self.environment.Q_values[4]).transpose()

    def append_Q_values(self):
        self.Q_crash = pd.concat([self.Q_crash, pd.DataFrame(self.environment.Q_values[0]).transpose()], ignore_index=True)
        self.Q_close = pd.concat([self.Q_close, pd.DataFrame(self.environment.Q_values[1]).transpose()], ignore_index=True)
        self.Q_nearby = pd.concat([self.Q_nearby, pd.DataFrame(self.environment.Q_values[2]).transpose()], ignore_index=True)
        self.Q_alone = pd.concat([self.Q_alone, pd.DataFrame(self.environment.Q_values[3]).transpose()], ignore_index=True)
        self.Q_lost = pd.concat([self.Q_lost, pd.DataFrame(self.environment.Q_values[4]).transpose()], ignore_index=True)
    
    def save_Q_values(self, track_version, obstacle_version):
        self.Q_crash.to_csv('q_values/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}_crash'.format(track_version, obstacle_version) + ".csv", index=False)
        self.Q_close.to_csv('q_values/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}_close'.format(track_version, obstacle_version) + ".csv", index=False)
        self.Q_nearby.to_csv('q_values/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}_nearby'.format(track_version, obstacle_version) + ".csv",  index=False)
        self.Q_alone.to_csv('q_values/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}_alone'.format(track_version, obstacle_version) + ".csv", index=False)
        self.Q_lost.to_csv('q_values/' + self.agent_name.lower().replace(' ', '_') + '_t{}o{}_lost'.format(track_version, obstacle_version) + ".csv", index=False)