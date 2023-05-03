import os
import pygame
import random
import math
from pygame import mixer # Para poner musica

# Todo lo que ocurra en una pantalla de pygame es un evento

# Iniciar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('alien_icon.png')
pygame.display.set_icon(icono)

# Agregar musica
mixer.music.load('sonido-fondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
sonido_disparo_on = False

# Imagen de fondo
fondo = pygame.image.load('Fondo.jpg')

# Variables del Jugador
img_jugador = pygame.image.load('penis.png')
jugador_x = 368  # Posicion X de la pantalla
jugador_y = 510  # Posicion Y de la pantalla
jugador_x_cambio = 0
jugador_y_cambio = 0

# Variables de Enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8
# Variables del Enemigo
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('vagina.png'))
    enemigo_x.append(random.randint(0, 736))  # Posicion X de la pantalla
    enemigo_y.append(random.randint(50, 200))  # Posicion Y de la pantalla
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

# Variables de Bala
img_bala = pygame.image.load('bala.png')
bala_x = 0  # Posicion X de la pantalla
bala_y = 525  # Posicion Y de la pantalla
bala_x_cambio = 0
bala_y_cambio = 0.5
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

# Sonido splash
def sonido_disparo():
    global sonido_disparo_on
    sonido_disparo_on = True
    sonido_disparo = mixer.Sound('sonido_splash.mp3')
    sonido_disparo.set_volume(0.3)
    sonido_disparo.play()

# Mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'LEFADAS: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))  # .blit Metodo para 'arrojar', en pantalla

# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))  # Para que la bala aparezca desde el centro de la nave

# Detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia <= 27:
        return True
    else:
        return False

def colision_con_jugador(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia <= 70:
        return True
    else:
        return False

def texto_final():
    puntaje_final = puntaje

    mi_fuente_final = fuente_final.render('LAS VAGINAS HAN GANADO', True, (255, 255, 255))
    mi_fuente_puntaje = fuente_final.render(f'LEFADAS: {puntaje_final}', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (120, 200))
    pantalla.blit(mi_fuente_puntaje, (260, 250))


# --------------------------------------------------

# Loop del juego || Se indica que el boton x cierre la ventana
se_ejecuta = True
while se_ejecuta:

    # Cambiar color fondo, dentro del loop
    pantalla.blit(fondo, (0, 0))

    # Iterar Eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:  # Si clic en X (Quit) se cierra
            se_ejecuta = False

        # Evento presioar teclas
        if evento.type == pygame.KEYDOWN:  # Evento, si una tecla cualquiera se presiona
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1  # Cambiar velocidad del movimiento (sumar posicion)
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:

                if not bala_visible:  # If bala_visible == False:
                    bala_x = jugador_x
                    disparar_bala(jugador_x, bala_y)
                    sonido_disparo()

        # Evento levantar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar la ubicacion jugador
    jugador_x += jugador_x_cambio  # Antes de que llame al def jugador() se le vincula con el movimiento

    # Mantener dentro de la pantalla al jugador
    if jugador_x <= 0:
        jugador_x = 0  # Asi no atraviesa la barrera de la izquierda
    elif jugador_x >= 736:
        jugador_x = 736  # Asi no atraviesa la barrera de la derecha
# ---------------------------------------------------------------
    # Modificar la ubicacion enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:  # Si llegan a bajo los enemigos pierdes
            for k in range(cantidad_enemigos):
                enemigo_y[e] = 1000
            texto_final()
            break
            # Colision jugador
        colision_jugador = colision_con_jugador(enemigo_y[e], enemigo_x[e], jugador_y, jugador_x)
        if colision_jugador:
            sonido_final = mixer.Sound('final.mp3')
            sonido_final.play()
            for c in range(cantidad_enemigos):
                enemigo_y[e] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro de la pantalla al enemgio
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)

        if colision:
            sonido_impacto = mixer.Sound('Golpe.mp3')
            sonido_impacto.set_volume(0.3)
            sonido_impacto.play()
            bala_y = 510
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)  # Posicion X de la pantalla
            enemigo_y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e], e)


    # Movimiento de la bala
    if bala_y <= -32:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)
    # Actualizar
    pygame.display.update()  # Actualizar pantalla para que se vea el fondo


#Hacer que el contador deje de contar tras perder

