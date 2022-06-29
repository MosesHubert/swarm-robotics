import pygame
import random
from matrix import *
from constants import *
from uiParameters import *
from agg_sim import Simulator

speed = 0.005
fps = 60
n = 4

flock = []
for i in range(n):
	flock.append(Simulator())

for boid in flock:
	boid.create_Q()

episodes = 100 # jumlah episode

for episode in range(episodes):
	pygame.init()
	window = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	textI = "10"
	reset = False
	SpaceButtonPressed = False
	backSpace = False
	keyPressed = False
	showUI = False
	clicked = False
	run = True
	sim_time = 600 # 1 episode = 10 detik

	for boid in flock:
		boid.start(random.randint(50, Width-50), random.randint(50, Height-50))
		boid.current_state(flock, Width, Height)
		boid.get_next_action()

	print("Agent 1 (Episode {})".format(episode+1))
	flock[0].terminal_output()
	print("")

	print("Agent 2 (Episode {})".format(episode+1))
	flock[1].terminal_output()
	print("")

	print("Agent 3 (Episode {})".format(episode+1))
	flock[2].terminal_output()
	print("")

	print("Agent 4 (Episode {})".format(episode+1))
	flock[3].terminal_output()
	print("")

	while run:
		aggregate = 0
		clock.tick(fps)
		window.fill((10, 10, 15))

		n = numberInput.value

		if reset == True or resetButton.state == True:
			flock = []
			for i in range(n):
				flock.append(Simulator())
			for boid in flock:
				boid.create_Q()
			reset = False

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
			print("Agent 1 (Episode {})".format(episode+1))
			flock[0].terminal_output()
		# print(q_values1)
			print("")

		q_values2 = flock[1].update_Q()
		if flock[1].is_state_change():
			flock[1].get_next_action()
			print("Agent 2 (Episode {})".format(episode+1))
			flock[1].terminal_output()
		# print(q_values2)
			print("")

		q_values3 = flock[2].update_Q()
		if flock[2].is_state_change():
			flock[2].get_next_action()
			print("Agent 3 (Episode {})".format(episode+1))
			flock[2].terminal_output()
		# print(q_values3)
			print("")

		q_values4 = flock[3].update_Q()
		if flock[3].is_state_change():
			flock[3].get_next_action()
			print("Agent 4 (Episode {})".format(episode+1))
			flock[3].terminal_output()
		# print(q_values4)
			print("")

		for index, boid in enumerate(flock):
			name = "Agent " + str(index+1)
			boid.Draw(screen=window, agent_name=name)

		if aggregate == 4:
			print("Konstanta aggregate: {}\n".format(aggregate))
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
	
	print("==============================================\n")

	pygame.quit()