
import pygame as pg
from enemigo import * 
from bullet import *
from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador
from plataforma import *
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
font = pg.font.Font(None, 36)  
clock = pg.time.Clock()

back_image = pg.image.load('assets\\img\\background\\background1.png')
back_image = pg.transform.scale(back_image, (ANCHO_VENTANA, ALTO_VENTANA))



game_running = True

main_player = Jugador(0, 0, frame_rate=200, speed_walk=20, speed_run=40)
enemigo = Enemy(x=450,y=400,speed_walk=6,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300)
lista_enemigos = [enemigo]

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

tiempo_transcurrido_generacion = 0
intervalo_generacion_enemigo = 3000 # 5000 ms (5 segundos)

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
    
    if lista_teclas_presionadas[pg.K_SPACE]: 
        main_player.shot()
       
    

    screen.blit(back_image, back_image.get_rect())
    delta_ms = clock.tick(FPS)


    enemigo.update(delta_ms,lista_plataformas, lista_balas)
    enemigo.draw(screen)
    
    main_player.update(delta_ms, lista_plataformas)
    main_player.draw(screen)
    
    for enemy in lista_enemigos:
        main_player.handle_enemy_collision(enemy)

        enemy.update(delta_ms, lista_plataformas, lista_balas)
        enemy.draw(screen)
        
    for bullet in lista_balas:
        bullet.update(delta_ms, lista_plataformas, lista_enemigos, main_player)
        bullet.draw(screen)

    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    tiempo_transcurrido_generacion += delta_ms
    if tiempo_transcurrido_generacion >= intervalo_generacion_enemigo:
        tiempo_transcurrido_generacion = 0
        enemigo.enemies_generator(lista_enemigos, 0)
    
    text = font.render(f'Vidas: {main_player.current_lifes}', True, (255, 255, 255))
    screen.blit(text, (10, 10))  # Ajusta la posición según tus necesidades

    pg.display.update()

pg.quit()