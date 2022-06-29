import pygame
import random
from matrix import *
from constants import *
from uiParameters import *
from coor_sim import Simulator

pygame.init()
speed = 0.005
fps = 60
n = 4

flock = []
for i in range(n):
	name = "Agent " + str(i+1)
	flock.append(Simulator(agent_name=name))

for boid in flock:
	boid.create_Q()

episodes = 100 # jumlah episode

print('\nSTART SIMULATION')
print("\n==============================================\n")

for episode in range(episodes):
	pygame.init()
	window = pygame.display.set_mode(size)
	clock = pygame.time.Clock()
	window.fill((10, 10, 15))

	textI = "10"
	reset = False
	SpaceButtonPressed = False
	backSpace = False
	keyPressed = False
	showUI = False
	clicked = False
	run = True
	sim_time = 900 # 1 episode = 15 detik

	flock[0].start(200,320)
	flock[1].start(200,400)
	flock[2].start(120,320)
	flock[3].start(120,400)

	for boid in flock:
		boid.current_state(flock, Width, Height)
		boid.get_next_action()

	str_terminal1 = flock[0].terminal_output()
	print(f"Agent 1 (Episode {episode+1}) =>\t" + str_terminal1)

	str_terminal2 = flock[1].terminal_output()
	print(f"Agent 2 (Episode {episode+1}) =>\t" + str_terminal2)

	str_terminal3 = flock[2].terminal_output()
	print(f"Agent 3 (Episode {episode+1}) =>\t" + str_terminal3)

	str_terminal4 = flock[3].terminal_output()
	print(f"Agent 4 (Episode {episode+1}) =>\t" + str_terminal4)

	while run:
		aggregate = 0
		clock.tick(fps)
		window.fill((10, 10, 15))

		n = numberInput.value

		flock[0].draw_target(window)

		for boid in flock:
			boid.behaviour(Width, Height)
			boid.current_state(flock, Width, Height)
			boid.update_action(flock)
			boid.crashing(flock)
			boid.update()
			boid.next_state(flock, Width, Height)
			aggregate += boid.is_terminal_state(flock)

		q_values1 = flock[0].update_Q()
		if flock[0].is_state_change():
			flock[0].get_next_action()
			str_terminal1 = flock[0].terminal_output()
			print(f"Agent 1 (Episode {episode+1}) =>\t" + str_terminal1)

		q_values2 = flock[1].update_Q()
		if flock[1].is_state_change():
			flock[1].get_next_action()
			str_terminal2 = flock[1].terminal_output()
			print(f"Agent 2 (Episode {episode+1}) =>\t" + str_terminal2)

		q_values3 = flock[2].update_Q()
		if flock[2].is_state_change():
			flock[2].get_next_action()
			str_terminal3 = flock[2].terminal_output()
			print(f"Agent 3 (Episode {episode+1}) =>\t" + str_terminal3)

		q_values4 = flock[3].update_Q()
		if flock[3].is_state_change():
			flock[3].get_next_action()
			str_terminal4 = flock[3].terminal_output()
			print(f"Agent 4 (Episode {episode+1}) =>\t" + str_terminal4)

		for boid in flock:
			boid.Draw(window)

		if aggregate == 4:
			print("Agregasi terjadi pada daerah target.")
			run = False

		sim_time -= 1
		if sim_time == 0:
			run = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONUP:
				clicked = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
				if event.key == pygame.K_r:
					reset = True
				if event.key == pygame.K_SPACE:
					SpaceButtonPressed = True

				textI = pygame.key.name(event.key)
				keyPressed = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_BACKSPACE:
					backSpace = True
				if event.key == pygame.K_u:
					showUI = not showUI
		
		backSpace = False
		keyPressed = False
		pygame.display.flip()
		clicked = False
	
	print("\n==============================================\n")

	pygame.quit()