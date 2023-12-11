import Nivel
from items import ItemBox
from plataforma import Plataform
from enemigo import Enemy
from Nivel import Nivel
class Nivel2(Nivel):
    def __init__(self):
        items = [ItemBox('Key', 600, 200), ItemBox('Book', 300, 100)]
        plataformas = [Plataform(100, 200, 150, 20), Plataform(400, 300, 120, 20), Plataform(600, 400, 100, 20)]
        enemigos = [Enemy(x=200, y=300, speed_walk=8, gravity=12, jump_power=25, frame_rate_ms=180,
                          move_rate_ms=40, jump_height=120, p_scale=0.1, interval_time_jump=250)]

        super().__init__(items, plataformas, enemigos)