import pygame

class Simulation:

    def __init__(self,population,fps,episodes,size) -> None:
        self.fps = fps
        self.episodes = episodes
        self.population = population

        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.window.fill((10,10,15))
        self.clock = pygame.time.Clock()
        self.is_running = True
    
    def __process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def __learning(self):
        pass

    def __update(self):
        pass

    def __render(self):
        pass

    def run(self):
        while self.is_running:
            self.__process_input()
            self.__learning()
            self.__update()
            self.__render()
