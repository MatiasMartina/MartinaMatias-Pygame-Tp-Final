from items import *
from chronometer import * 
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

main_player = Jugador(0, 0, frame_rate=200, speed_walk=15, speed_run=20)
enemigo = Enemy(x=450,y=400,speed_walk=6,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300)
lista_enemigos = [enemigo]
item_box = ItemBox('Time', 400, 410)
item_box2= ItemBox('Portal', 150, 60)
item_box3= ItemBox('Heart', 700, 410)
item_box4= ItemBox('Book', 700, 330)
item_box5= ItemBox('Boot', 300, 330)
item_box6 = ItemBox('Key', 900, 400)


lista_items = [item_box, item_box2, item_box3, item_box4, item_box5, item_box6]
plataforma1 = Plataform(100, 100, 100, 20)
plataforma2 = Plataform(200, 400, 100, 20)
plataforma3 = Plataform(350, 300, 100, 20)
plataforma4 = Plataform(700, 400, 100, 20)
plataforma5 = Plataform(650, 300, 100, 20)
# plataforma6 = Plataform(200, 500, 100, 20)
# plataforma7 = Plataform(400, 450, 100, 20)
plataforma8 = Plataform(600, 400, 100, 20)
plataforma9 = Plataform(800, 350, 100, 20)
plataforma10 = Plataform(1000, 300, 100, 20)


lista_balas = Jugador.lista_balas
lista_plataformas = [plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma8, plataforma9, plataforma10]
chronometer = Chronometer(60)
tiempo_transcurrido_generacion = 0
intervalo_generacion_enemigo = 10000 # 5000 ms (5 segundos)

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

    
    chronometer.update()
    chronometer.draw(screen)

    enemigo.update(delta_ms,lista_plataformas, lista_balas, lista_enemigos,main_player)
    enemigo.draw(screen, lista_balas)
    
    main_player.update(delta_ms, lista_plataformas, lista_enemigos,lista_balas, enemigo)
    main_player.draw(screen)
    
    
        
    for bullet in lista_balas:
        bullet.update(delta_ms, lista_plataformas, lista_enemigos, main_player)
        bullet.draw(screen, lista_balas)

    for enemy in lista_enemigos:
        if enemy in lista_enemigos:
            # main_player.handle_enemy_collision(enemy)

            enemy.update(delta_ms, lista_plataformas, lista_balas, lista_enemigos, main_player)
            enemy.draw(screen, lista_balas)
    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    for item in lista_items:
        print(f"Item Type: {item.item_type}, Position: ({item.coor_x}, {item.coor_y})")
        item.update(main_player, lista_items, chronometer,screen, 700,500)
        item.draw(screen)

    # tiempo_transcurrido_generacion += delta_ms
    # if tiempo_transcurrido_generacion >= intervalo_generacion_enemigo:
    #     tiempo_transcurrido_generacion = 0
    #     enemigo.enemies_generator(lista_enemigos, 0)
    
    text = font.render(f'Vidas: {main_player.current_lifes}', True, (255, 255, 255))
    # text_score = font.render(f'Puntaje: {main_player.score}', True, (255, 255, 255))
    screen.blit(text, (10, 10))  
    font = pg.font.Font(None, 36)  # Fuente y tamaño del texto
    score_text = font.render(f"Score: {main_player.score}", True, (255, 255, 255))  # Crear el objeto de texto
    screen.blit(score_text, (50, 50))  # Mostrar el texto en la posición deseada
    # screen.blit(text_score, (10, 50))
    pg.display.update()

pg.quit()