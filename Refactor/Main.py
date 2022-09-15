import Swarm_BB8
from Swarm_BB8.Agent import Agent

if __name__ == "__main__":
    agents = []
    for i in range(5):
        agents.append(Agent())
    
    ids = agents[1].get_nearby(agents)
    print(ids)