from Simulation import Simulation

fps = 60
episodes = 100
population = 4
size = [400,300]
sim = Simulation(population,fps,episodes,size)

sim.run()