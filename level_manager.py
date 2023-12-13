from pygame.locals import *
from level1 import Level1
from level2 import Level2
from level3 import Level3

class Level_manager:
    def __init__(self, screen):
        self.slave = screen
        self.levels = {'level_one':Level1, 'level_two': Level2, 'level_three' : Level3}

        pass
    def get_level(self, level_name):
        return self.levels[level_name](self.slave)