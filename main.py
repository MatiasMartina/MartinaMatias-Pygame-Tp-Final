import pygame as pg
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player_copy import Jugador
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()

clock = pg.time.Clock()

back_image = pg.image.load('assets\\img\\background\\background1.png')
back_image = pg.transform.scale(back_image,(ANCHO_VENTANA, ALTO_VENTANA))


game_running = True

main_player = Jugador(0,0, frame_rate= 100, speed_walk = 20, speed_run= 40)

while game_running:
    

    lista_eventos = pg.event.get()
    for event in lista_eventos:
        # if event.type == pg.K_SPACE:
        #     main_player.jump()
        if event.type == pg.QUIT:
            game_running = False

    lista_teclas_presionadas = pg.key.get_pressed()
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        main_player.walk('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        main_player.walk('Left')
    if not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        main_player.stay()
    if lista_teclas_presionadas[pg.K_RIGHT] and lista_teclas_presionadas[pg.K_LSHIFT]:     
        main_player.run('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_LSHIFT]:
        main_player.run('Left')
    if lista_teclas_presionadas[pg.K_SPACE]:
        main_player.jump()



    screen.blit(back_image, back_image.get_rect())
    delta_ms = clock.tick(FPS)
    main_player.update(delta_ms)
    main_player.draw(screen)

    pg.display.update()

pg.quit()