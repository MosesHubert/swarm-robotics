import pygame
from simulation.Matrix import *

class Sensor:
    def __init__(self, arena, agent_name, inner, outer, text_font, agent_text_size, agent_color, agent_size, angle, stroke=5):
        self.arena = arena
        self.agent_name = agent_name
        self.inner_sensor = inner
        self.outer_sensor = outer
        self.text_font = text_font
        self.agent_color = agent_color
        self.agent_text_size = agent_text_size
        self.font_agent = pygame.font.SysFont(text_font, agent_text_size)
        self.text_agent = self.font_agent.render(agent_name, False, agent_color)
        self.agent_size = agent_size
        self.stroke = stroke
        self.angle = angle
        
    def draw_sensor(self, agent_position, state, action, mode, inner_color, outer_color, agent_head_color, state_color, action_color, mode_color, angle, distance=5, scale=2):
        self.angle = angle
        ps = []
        points = [None for _ in range(3)]
        
        points[0] = [[0],[-self.agent_size],[0]]
        points[1] = [[self.agent_size//2],[self.agent_size//2],[0]]
        points[2] = [[-self.agent_size//2],[self.agent_size//2],[0]]
        
        for point in points:
            rotated = matrix_multiplication(rotationZ(self.angle) , point)
            z = 1/(distance - rotated[2][0])
            
            projection_matrix = [[z, 0, 0], [0, z, 0]]
            projected_2d = matrix_multiplication(projection_matrix, rotated)
            
            x = int(projected_2d[0][0] * scale) + agent_position.x
            y = int(projected_2d[1][0] * scale) + agent_position.y
            ps.append((x, y))

        pygame.draw.circle(self.arena.surface, outer_color, (agent_position.x, agent_position.y), self.outer_sensor, width=1)
        pygame.draw.circle(self.arena.surface, inner_color, (agent_position.x, agent_position.y), self.inner_sensor, width=1)
        my_font = pygame.font.SysFont(self.text_font, self.agent_text_size)
        text_state = my_font.render(state, False, state_color)
        text_action = my_font.render(action, False, action_color)
        text_mode = my_font.render(mode, False, mode_color)
        self.arena.surface.blit(self.text_agent, (agent_position.x-20, agent_position.y-35))
        self.arena.surface.blit(text_state, (agent_position.x+28, agent_position.y-15))
        self.arena.surface.blit(text_action, (agent_position.x+28, agent_position.y))
        self.arena.surface.blit(text_mode, (agent_position.x-28, agent_position.y+25))
        pygame.draw.circle(self.arena.surface, self.agent_color, (agent_position.x, agent_position.y), self.agent_size)
        pygame.draw.polygon(self.arena.surface, agent_head_color, ps, self.stroke)