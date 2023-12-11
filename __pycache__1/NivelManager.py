from Nivel1 import Nivel1
from Nivel2 import Nivel2
from Nivel3 import Nivel3
from items import ItemBox
from plataforma import Plataform
from enemigo import Enemy
from Nivel import Nivel

class NivelManager:
    def __init__(self):
        self.niveles = [Nivel1(), Nivel2(), Nivel3()]
        self.nivel_actual = 0

    def cambiar_nivel(self):
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1
        else:
            print("¡Has completado todos los niveles!")

    def update(self, delta_ms):
        self.niveles[self.nivel_actual].update(delta_ms)

    def draw(self, screen):
        self.niveles[self.nivel_actual].draw(screen)

    def iniciar_juego(self, screen,lista_balas):
        # Configuración inicial del juego con el primer nivel
        self.nivel_actual = 0
        self.niveles[self.nivel_actual].iniciar_nivel(screen, lista_balas)