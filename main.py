import pygame as pg
from bullet import *
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador
from plataforma import *
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()

clock = pg.time.Clock()

back_image = pg.image.load('assets\\img\\background\\background1.png')
back_image = pg.transform.scale(back_image, (ANCHO_VENTANA, ALTO_VENTANA))



game_running = True

main_player = Jugador(0, 0, frame_rate=200, speed_walk=20, speed_run=40)
plataforma1 = Plataform(300, 400, 100, 20)
plataforma2 = Plataform(200, 400, 100, 20)
plataforma3 = Plataform(350, 300, 100, 20)
plataforma4 = Plataform(700, 400, 100, 20)
plataforma5 = Plataform(650, 300, 100, 20)
# plataforma6 = Plataform(200, 500, 100, 20)
plataforma7 = Plataform(400, 450, 100, 20)
plataforma8 = Plataform(600, 400, 100, 20)
plataforma9 = Plataform(800, 350, 100, 20)
plataforma10 = Plataform(1000, 300, 100, 20)


lista_balas = Jugador.lista_balas
lista_plataformas = [plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma7, plataforma8, plataforma9, plataforma10]

while game_running:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                print("Está acá")
                main_player.jump(delta_ms)

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
    # if lista_teclas_presionadas[pg.K_UP]:
    #     main_player.jump(delta_ms)
    if lista_teclas_presionadas[pg.K_SPACE]:
        main_player.shot()
       
    

    screen.blit(back_image, back_image.get_rect())
    delta_ms = clock.tick(FPS)
    main_player.update(delta_ms, lista_plataformas)
    # main_player.handle_collision(plataforma1)
    # main_player.handle_collision(plataforma2)
    # # main_player.handle_collision(plataforma3)
    # main_player.handle_collision(plataforma4)
    # main_player.handle_collision(plataforma5)
    main_player.draw(screen)
    plataforma1.draw(screen)
    plataforma2.draw(screen)
    plataforma3.draw(screen)
    plataforma4.draw(screen)
    plataforma5.draw(screen)
    
    plataforma7.draw(screen)
    plataforma8.draw(screen)
    plataforma9.draw(screen)
    plataforma10.draw(screen)
    for bullet in lista_balas:
        bullet.update(delta_ms, [], [], main_player)
        bullet.draw(screen)
    pg.display.update()

pg.quit()