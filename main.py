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

lista_balas = []

game_running = True

main_player = Jugador(0, 0, frame_rate=100, speed_walk=20, speed_run=40)
plataforma1 = Plataform(300, 400, 100, 20)  
plataforma2 = Plataform(200, 400, 100, 20)  
# plataforma3 = Plataform(350, 300, 100, 20)  
plataforma4 = Plataform(700, 400, 100, 20)  
# plataforma5 = Plataform(650, 300, 100, 20)  


lista_balas = Jugador.lista_balas


while game_running:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                print("Está acá")
                main_player.shot()

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
    if lista_teclas_presionadas[pg.K_UP]:
        main_player.jump()
    if lista_teclas_presionadas[pg.K_SPACE]:
        main_player.shot()
       
    

    screen.blit(back_image, back_image.get_rect())
    delta_ms = clock.tick(FPS)
    main_player.update(delta_ms)
    main_player.handle_collision(plataforma1)
    main_player.handle_collision(plataforma2)
    # main_player.handle_collision(plataforma3)
    main_player.handle_collision(plataforma4)
    # main_player.handle_collision(plataforma5)
    main_player.draw(screen)
    plataforma1.draw(screen)
    plataforma2.draw(screen)
    # plataforma3.draw(screen)
    plataforma4.draw(screen)
    # plataforma5.draw(screen)
    for bullet in lista_balas:
        bullet.update(delta_ms, [], [], main_player)
        bullet.draw(screen)
    pg.display.update()

pg.quit()