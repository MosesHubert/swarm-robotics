import pygame

class Arena:
    def __init__(self, width, height, text_font, obstacle_text_size, terminal_text_size, episode_text_size, text_color):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.font_obstacle = pygame.font.SysFont(text_font, obstacle_text_size, bold=True)
        self.font_terminal = pygame.font.SysFont(text_font, terminal_text_size, bold=True)
        self.font_episode = pygame.font.SysFont(text_font, episode_text_size, bold=True)
        self.text_obstacle = self.font_obstacle.render('OBSTACLE', False, text_color)
        self.text_start = self.font_terminal.render('START', False, text_color)
        self.text_target = self.font_terminal.render('TARGET', False, text_color)

    def draw_arena(self, arena_color):
        self.surface.fill(arena_color)

    def draw_circle(self, obstacle_color, terminal_color, obstacle_radius, terminal_radius, obstacle_position, start_position, target_position):
        pygame.draw.circle(self.surface, obstacle_color, obstacle_position, obstacle_radius)
        pygame.draw.circle(self.surface, terminal_color, target_position, terminal_radius)
        pygame.draw.circle(self.surface, terminal_color, start_position, terminal_radius)

    def draw_text(self, obstacle_text_position, start_text_position, target_text_position, episode_text_position, episode_text_color, episode):
        self.text_episode = self.font_episode.render('Episode {}'.format(episode+1), False, episode_text_color)
        self.surface.blit(self.text_obstacle, obstacle_text_position)
        self.surface.blit(self.text_start, start_text_position)
        self.surface.blit(self.text_target, target_text_position)
        self.surface.blit(self.text_episode, episode_text_position)

    def render(self, fps):
        pygame.display.update()
        self.clock.tick(fps)