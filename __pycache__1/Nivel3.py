import Nivel
from items import ItemBox
from plataforma import Plataform
from enemigo import Enemy
from Nivel import Nivel
class Nivel3(Nivel):
    def __init__(self):
        items = [ItemBox('Book', 200, 350), ItemBox('Book', 800, 200)]
        plataformas = [Plataform(150, 150, 100, 20), Plataform(350, 300, 150, 20), Plataform(700, 400, 120, 20)]
        enemigos = [Enemy(x=500, y=200, speed_walk=7, gravity=15, jump_power=28, frame_rate_ms=160,
                          move_rate_ms=45, jump_height=130, p_scale=0.09, interval_time_jump=280)]

        super().__init__(items, plataformas, enemigos)