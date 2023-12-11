import Nivel
from items import ItemBox
from plataforma import Plataform
from enemigo import Enemy
from Nivel import Nivel
class Nivel1(Nivel):
    def __init__(self):
        items = [ItemBox('Time', 400, 410), ItemBox('Book', 150, 60)]
        plataformas = [Plataform(100, 100, 100, 20), Plataform(200, 400, 100, 20), Plataform(350, 300, 100, 20)]
        enemigos = [Enemy(x=450, y=400, speed_walk=6, gravity=14, jump_power=30, frame_rate_ms=150,
                          move_rate_ms=50, jump_height=140, p_scale=0.08, interval_time_jump=300)]

        super().__init__(items, plataformas, enemigos)

    def iniciar_nivel(self,screen,lista_balas):
        self.items[0].coor_x = 400
        self.items[0].coor_y = 410

        self.items[1].coor_x = 150
        self.items[1].coor_y = 60

        self.plataformas[0].coor_x = 100
        self.plataformas[0].coor_y = 100

        self.plataformas[1].coor_x = 200
        self.plataformas[1].coor_y = 400

        self.plataformas[2].coor_x = 350
        self.plataformas[2].coor_y = 300
        
        self.draw(screen, lista_balas)
    def draw(self, screen, lista_balas):
    # Dibujar elementos del nivel en la pantalla
        for item in self.items:
            item.draw(screen)

        for plataforma in self.plataformas:
            plataforma.draw(screen)

        for enemigo in self.enemigos:
            enemigo.draw(screen, lista_balas)