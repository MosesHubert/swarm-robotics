import pygame
from parameters2 import *
from simulation import Agent, Arena

# initialization
arena = Arena(width, height, text_font, obstacle_text_size, terminal_text_size, episode_text_size, text_color)
agents = []
num_data_x = [red_buffer, green_buffer]
for agent, target in zip(range(number_of_agents), target_positions):
    agent_name = "Agent " + str(agent+1)
    agents.append(Agent(arena, agents, num_data_x[agent], width, height, agent_name, target[0], target[1], inner, outer, max_speed, max_length,
                        starting_angle, obstacle_position, obstacle_radius, text_font, agent_text_size, white, radius, epsilon, learning_rate, 
                        discount_factor, separation_magnitude, alignment_magnitude, cohesion_magnitude))
dynamics_attribute = [[Kp_red, Ki_red, a0_red, a1_red, b1_red],
                      [Kp_green, Ki_green, a0_green, a1_green, b1_green]]

# simulation
simulation_time = 0
run_simulation = True
episodes = number_of_episodes
print('\n------------- Start Simulation -------------\n')

for episode in range(episodes):
    run_episode = True
    is_terminal = number_of_agents
    time_limit = episode_time * frame_per_second

    # reset agent position
    for agent, starting_position in zip(agents, starting_positions):
        agent.reset(starting_position[0], starting_position[1])

    # get initial state and action
    for agent in agents:
        agent.get_first_state_action(agent)
        agent.show_output(episode)

    while run_episode:
        arena.render(frame_per_second)
        arena.draw_arena(black)
        arena.draw_circle(obstacle_color, terminal_color, obstacle_radius, terminal_radius, obstacle_position, start_position, target_position)
        arena.draw_text(obstacle_text_position, start_text_position, target_text_position, episode_text_position, episode_text_color, episode)

        # get old state and update acceleration based on behavior and action
        for agent in agents:
            agent.get_current_state(agent)
            agent.update_acceleration(agent, agents, wander_magnitude, avoid_magnitude, target_magnitude)

        # update position and velocity
        time_interval = 0.035 # timeit.timeit()
        for agent, dynamic in zip(agents, dynamics_attribute):
            agent.update_kinematics(dynamic[0], dynamic[1], dynamic[2], dynamic[3], dynamic[4], time_interval)

        # get new state and new action, update Q-values, and draw agents
        for agent in agents:
            agent.get_next_state(agent)
            agent.get_next_action()
            agent.update_matrix_values(episode, track_version, obstacle_version)
            agent.draw_agent(red, green, black, yellow, blue, orange)
            is_terminal -= agent.is_terminal_state(agents)

        # time.sleep(time_interval)

        if is_terminal == 0:
            run_episode = False

        time_limit -= 1
        if time_limit == 0:
            run_episode = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_episode = False
                run_simulation = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_episode = False
                    run_simulation = False
                if event.key == pygame.K_q:
                    run_episode = False
        
    print('\n------------- End of Episode {} -------------\n'.format(episode+1))
    if not run_simulation:
        break

pygame.quit()