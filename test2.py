import cv2
import time
import pygame
import threading
import numpy as np
from testParameters2 import *
from simulation.Vector import *
from implementation import BB8_driver
from implementation.VirtualArena import VirtualArena
from implementation.VirtualAgent import VirtualAgent

run = True
cx_red = 0
cy_red = 0
cx_green = 0
cy_green = 0
velocity_red = 0
velocity_green = 0
delta_time = 0

# tersambung dengan BB-8 merah
bb8_red = BB8_driver.Sphero('CC:05:3A:B6:A2:AE')
bb8_red.connect()
bb8_red.start()
time.sleep(1.0)
bb8_red.set_rgb_led(240, 30, 0, 0, True)
print("\nRobot merah siap.\n")

# tersambung dengan BB-8 hijau
bb8_green = BB8_driver.Sphero('C8:88:28:09:8F:1D')
bb8_green.connect()
bb8_green.start()
time.sleep(1.0)
bb8_green.set_rgb_led(0, 230, 140, 0, True)
print("\nRobot hijau siap.\n")

def sensor():

    # inisialisasi parameter global
    global run
    global cx_red
    global cy_red
    global cx_green
    global cy_green
    global velocity_red
    global velocity_green
    global delta_time

    # inisialisasi parameter kinematika
    previous_time = 0
    current_time = 0
    previous_position_red = None
    previous_position_green = None

    # tersambung dengan kamera
    kamera = cv2.VideoCapture(2)
    _,frame = kamera.read()
    timestamp_now = kamera.get(cv2.CAP_PROP_POS_MSEC)

    while run:
        # start camera and get position
        _,frame = kamera.read()
        timestamp = kamera.get(cv2.CAP_PROP_POS_MSEC)
        delta_time = (timestamp - timestamp_now) * 0.001
        timestamp_now = timestamp
        frame = cv2.blur(frame,(4,4))

        # kernel erosion-dilation
        kernel_eros = np.ones((5,5), np.uint8)
        kernel_dil = np.ones((5,5), np.uint8)

        ########## IDENTIFIKASI BB-8 MERAH ##########

        # threshold warna merah
        hsv_red = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_red = np.array([0, 50, 50])
        high_red = np.array([20, 255, 255])
        thresh_red = cv2.inRange(hsv_red, low_red, high_red)

        # erosion-dilation
        dil_red = cv2.dilate(thresh_red, kernel_dil, iterations=2)
        eros_red = cv2.erode(dil_red, kernel_eros, iterations=1)

        # menemukan kontur
        _, kontur_red, _ = cv2.findContours(eros_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # menemukan titik tengah dari kontur
        area_maksimal_red = 0
        pusat_titik_red = 1
        for pusat_red in kontur_red:
            area_red = cv2.contourArea(pusat_red)
            if area_red > area_maksimal_red:
                area_maksimal_red = area_red
                pusat_titik_red = pusat_red

        M_red = cv2.moments(pusat_titik_red)
        cx_red, cy_red = int(M_red['m10']/M_red['m00']), int(M_red['m01']/M_red['m00'])

        ########## IDENTIFIKASI BB-8 HIJAU ##########

        # threshold warna hijau
        hsv_green = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_green = np.array([50, 25, 25])
        high_green = np.array([90, 255, 255])
        thresh_green = cv2.inRange(hsv_green, low_green, high_green)

        # erosion-dilation
        # eros_green = cv2.erode(thresh_green, kernel_eros, iterations=1)
        dil_green = cv2.dilate(thresh_green, kernel_dil, iterations=2)

        # menemukan kontur
        _, kontur_green, _ = cv2.findContours(dil_green,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # menemukan titik tengah dari kontur
        area_maksimal_green = 0
        pusat_titik_green = 1
        for pusat_green in kontur_green:
            area_green = cv2.contourArea(pusat_green)
            if area_green > area_maksimal_green:
                area_maksimal_green = area_green
                pusat_titik_green = pusat_green

        M_green = cv2.moments(pusat_titik_green)
        cx_green, cy_green = int(M_green['m10']/M_green['m00']), int(M_green['m01']/M_green['m00'])

        ########## MENAMPILKAN HASIL ##########
        
        cv2.circle(frame, (cx_red, cy_red), 10, 255, -1)
        cv2.circle(frame, (cx_green, cy_green), 10, 255, -1)
        cv2.imshow('Real', frame)
        cv2.imshow('BB-8 Merah', eros_red)
        cv2.imshow('BB-8 Hijau', dil_green)

        ########## MENGHITUNG KECEPATAN ##########

        current_time += delta_time
        current_position_red = Vector(cx_red, cy_red)
        current_position_green = Vector(cx_green, cy_green)

        if previous_position_red is not None:
            velocity_red = getDistance(current_position_red, previous_position_red) / (current_time - previous_time)
            velocity_red = velocity_red * 0.3683 * 0.01
        else:
            velocity_red = 0

        if previous_position_green is not None:
            velocity_green = getDistance(current_position_green, previous_position_green) / (current_time - previous_time)
            velocity_green = velocity_green * 0.3683 * 0.01
        else:
            velocity_green = 0

        previous_position_red = current_position_red
        previous_position_green = current_position_green
        previous_time = current_time

        k = cv2.waitKey(1)
        if k % 256 == 27:
            run = False

def virtual_sensor():

    # delay to start
    time.sleep(1.0)

    # inisialisasi parameter global
    global run
    global cx_red
    global cy_red
    global cx_green
    global cy_green
    global velocity_red
    global velocity_green
    global delta_time

    # inisialisasi parameter pygame
    arena = VirtualArena(width, height, text_font, obstacle_text_size, terminal_text_size, testing_text_size, text_color, testing_text_color)
    agents = []
    controller_attribute = [[bb8_red, Kp_red, Ki_red],[bb8_green, Kp_green, Ki_green]]
    for agent, target, control in zip(range(number_of_agents), target_positions, controller_attribute):
        agent_name = "Agent " + str(agent+1)
        agents.append(VirtualAgent(arena, control[0], agents, '{}_t{}o{}'.format(agent+1, track_version, obstacle_version), width, height, agent_name, target[0], target[1], inner, outer, max_speed, max_length,
                                starting_angle, obstacle_position, obstacle_radius, text_font, agent_text_size, white, radius, epsilon, learning_rate, 
                                discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude))
    is_terminal = number_of_agents
    first = True

    for agent in agents:
        agent.reset()

    while run:
        # arena pygame
        arena.render(frame_per_second)
        arena.draw_arena(black)
        arena.draw_circle(obstacle_color, terminal_color, obstacle_radius, terminal_radius, obstacle_position, start_position, target_position)
        arena.draw_text(obstacle_text_position, start_text_position, target_text_position, testing_text_position)

        # get real position
        positions = [[cx_red, cy_red], [cx_green, cy_green]]        

        # get first state and action
        if first:
            for agent, position in zip(agents, positions):
                agent.get_position(position[0], position[1])
                agent.get_first_state_action(agent)
                agent.show_output()
            first = False

        # get old state and update acceleration based on behavior and action
        for agent in agents:
            agent.get_current_state(agent)
            agent.update_acceleration(agent, agents, wander_magnitude, avoid_magnitude, target_magnitude)

        # get real velocity
        velocities = [velocity_red, velocity_green]

        # update position and velocity
        for agent, control, velocity, position in zip(agents, controller_attribute, velocities, positions):
            agent.update_kinematics(velocity, control[1], control[2], delta_time)
            agent.get_position(position[0], position[1])

        # get new state and new action, update Q-values, and draw agents
        for agent in agents:
            agent.get_next_state(agent)
            agent.get_next_action()
            agent.draw_agent(red, green, black, yellow, blue, orange)
            is_terminal -= agent.is_terminal_state(agents)

        # terminal state
        if is_terminal == 0:
            run = False

        # stop program
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    pygame.quit()

# menjalankan program dengan threading
if __name__ == "__main__":
    sensor = threading.Thread(target=sensor)
    sensor.start()
    virtual_sensor = threading.Thread(target=virtual_sensor)
    virtual_sensor.start()