import pygame

WHITE = "White"
BLACK= "Black"

class Chronometer:
    def __init__(self, initial_time) -> None:
        self.descending_time = initial_time
        self.minutes = 0
        self.source = pygame.font.SysFont("Forte", 40)
        self.actual_time = pygame.time.get_ticks()
        self.stoped = False
        self.colour = WHITE

    def update(self):
        if self.stoped == False:
            time_elapsed = pygame.time.get_ticks() - self.actual_time
            if time_elapsed >= 1000:
                self.actual_time = pygame.time.get_ticks()
                self.descending_time -= 1  # Resta 1 segundo en lugar de sumar 1


    def draw(self, screen):
        chronometer = self.source.render(f"0{self.minutes} : {str(self.descending_time).zfill(2)}", False, self.colour)
        screen.blit(chronometer, (870, 6))

    def get_time(self)-> int:
        return self.descending_time
