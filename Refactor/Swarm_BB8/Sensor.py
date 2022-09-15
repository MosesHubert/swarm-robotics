class Sensor:
    def __init__(self,position,inner_radius=50,outer_radius=90):
        self.position = position
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
    
    def update(self,position):
        self.position = position
    
    def get_nearby_agent(self,host,agents):
        ids = []
        for agent in agents:
            if host is not agent:
                distance = (agent.get_position() - self.position).magnitude()
                if distance <=self.inner_radius:
                    ids.append(agent.get_id())
        
        return ids