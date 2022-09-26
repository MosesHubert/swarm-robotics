from turtle import delay
from simulation.Vector import middle_point

# simulation parameters
number_of_agents   = 4
frame_per_second   = 30
number_of_episodes = 30
episode_time       = 6 # * 3 + 1 -> seconds
delta_time         = 0.1
loop_delay         = 0.09

# arena size
width, height = 639, 479

# version
track_version = int(input('Track version: ')) # insert 1 or 2
obstacle_version = int(input('Obstacle version: ')) # insert 1, 2, or 3

# agent characteristics
red_buffer = 2
green_buffer = 2
a0_red = 0.141 # x[k-2]
a1_red = 0.443 # x[k-1]
b1_red = 0.431 # y[k-1]
a0_green = 0.04345
a1_green = 0.3238
b1_green = 0.6239

# PID parameters
Kp_red = 1.288
Ki_red = 6.4445
Kp_green = 2.2728
Ki_green = 7.8173

# agent track version
'''
Adjusted to the number of agents.
'''
if track_version == 1:
    start_position = (160, 360)
    target_position = (480, 120)
    starting_positions = [
        # (120, 320), # agent 1
        # (200, 400)  # agent 2
        (210, 360), # agent 1
        (160, 310), # agent 2
        (160, 410), # agent 3
        (110, 360)  # agent 4
    ]
    target_positions = [
        # (450,  80), # agent 1
        # (510, 160)  # agent 2
        (530, 120), # agent 1
        (480,  70), # agent 2
        (480, 170), # agent 3
        (430, 120)  # agent 4
    ]
elif track_version == 2:
    start_position = (120, 240)
    target_position = (520, 240)
    starting_positions = [
        # (120, 200), # agent 1
        # (120, 280)  # agent 2
        (160, 280), # agent 1
        (160, 200), # agent 2
        ( 80, 280), # agent 3
        ( 80, 200)  # agent 4
    ]
    target_positions = [
        # (520, 190), # agent 1
        # (520, 290)  # agent 2
        (560, 280), # agent 1
        (560, 200), # agent 2
        (480, 280), # agent 3
        (480, 200)  # agent 4
    ]
else:
    raise Exception('Please insert 1 or 2.')

# obstacle version
if obstacle_version == 1:
    obstacle_radius = 60
    obstacle_text_size = 18
    obstacle_position = ((width+1)/2, (height+1)/2)
    obstacle_text_position = (obstacle_position[0] - 50, obstacle_position[1] - 5)
elif obstacle_version == 2:
    obstacle_radius = 40
    obstacle_text_size = 13
    obstacle_position = (middle_point(starting_positions[0][0], target_positions[2][0]),
                         middle_point(starting_positions[0][1], target_positions[2][1]))
    obstacle_text_position = (obstacle_position[0] - 35, obstacle_position[1] - 5)
elif obstacle_version == 3:
    obstacle_radius = 40
    obstacle_text_size = 13
    obstacle_position = (middle_point(starting_positions[1][0], target_positions[3][0]),
                         middle_point(starting_positions[1][1], target_positions[3][1]))
    obstacle_text_position = (obstacle_position[0] - 35, obstacle_position[1] - 5)
else:
    raise Exception('Please insert 1, 2, or 3.')

# agent parameters
radius = 20
max_speed_in_mps = 0.5
max_speed = max_speed_in_mps * 100 * 20 / 7.366
max_length = 1
starting_angle = 0

# q-learning parameters
epsilon = 0.1
learning_rate = 0.5
discount_factor = 0.8

# action parameters
separation_magnitude = 40
alignment_magnitude = 20
cohesion_magnitude = 20

# behavior parameters
wander_magnitude = 80
avoid_magnitude = 100
target_magnitude = 120

# color (in RGB)
white  = (225, 225, 225)
black  = ( 10,  10,  15)
red    = (150,   0,   0)
green  = (110, 255,  10)
yellow = (240, 240,   0)
blue   = ( 80, 180, 240)
orange = (210, 150, 100)
grey   = ( 30,  30,  30)

# sensor parameters
inner = 50
outer = 90

# drawing colors
obstacle_color = white
terminal_color = grey

# drawing radius
terminal_radius = 100

# text parameters
text_font  = 'Arial'
text_color = black
agent_text_size    = 12
terminal_text_size = 36
episode_text_size  = 32
episode_text_color = white

# text positions
start_text_position    = (start_position[0]-62, start_position[1]-15)
target_text_position   = (target_position[0]-70, target_position[1]-15)
episode_text_position  = (20, 20)