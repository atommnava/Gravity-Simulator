import math
import random
from math import cos, sin, sqrt
from random import randrange

import pygame

ANCHO = 1450
ALTURA = 900
CENTRO = ANCHO // 2, ALTURA // 2
centroX = ANCHO // 2
centroY = ALTURA // 2

# Agujero negro Campos
G = 0.2
M = 1e9

BLACK = (0, 0, 0)
WHITE = (255,255,255)

# Agujero negro
r0 = 25

pygame.init()


class Particula:
    def __init__(self, x, y):
        self.g = G
        self.mass = 2
        self.x = x
        self.y = y
        self.momentum_x = 0
        self.momentum_y = 0
        self.dt = 0.001

    def move(self, x_y_central_mass):
        x2 = x_y_central_mass[0]
        y2 = x_y_central_mass[1]
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = math.atan2(y2 - self.y, x2 - self.x)
        force = (self.g * self.mass * M) / hyp
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        self.momentum_x += force_x * self.dt
        self.momentum_y += force_y * self.dt
        self.x += self.momentum_x / self.mass * self.dt
        self.y += self.momentum_y / self.mass * self.dt

        return [self.x, self.y]




screen = pygame.display.set_mode((ANCHO, ALTURA))

particulas = []

r = 200


# Linea
""""
def generator():
    for i in range(1000):
        x = randrange(-500, 1000)
        y = 100
        p = Particula(x, y)
        particulas.append(p)
"""

# Circulo
"""
def generator():
     for i in range(1000):
         ang = random.uniform(0, 1) * 2 * math.pi
         hyp = sqrt(random.uniform(0, 1)) * r
         adj = cos(ang) * hyp
         opp = sin(ang) * hyp
         x = centroX + adj
         y = centroY + opp
         p = Particula(x, y)
         particulas.append(p)
"""

# Cuadrado
def generator():
     for i in range(20000):
         x = randrange(0, 500)
         y = randrange(0, 500)
         p = Particula(x, y)
         particulas.append(p)

# Flor
"""
def generator():
    petals = 6
    for i in range(20000):
        angulo = random.uniform(0, 2 * math.pi)
        radio = 150 + 50 * math.sin(petals * angulo)
        x = centroX + radio * cos(angulo)
        y = centroY + radio * sin(angulo)
        p = Particula(x, y)
        particulas.append(p)

"""
def TON618():
    for _ in range(25000):
        angulo = random.uniform(0, 2 * math.pi)
        radio = random.uniform(100, 250)
        x = centroX + radio * cos(angulo)
        y = centroY + radio * sin(angulo)
        p = Particula(x, y)
        # velocidad orbital pero incompleta
        speed = sqrt(G * M / radio) * 0.6  # 60% de la velocidad de escape
        p.momentum_x = -speed * sin(angulo)
        p.momentum_y = speed * cos(angulo)
        particulas.append(p)


TON618()
#generator()

def draw():
    for i in range(len(particulas)):
        pygame.draw.circle(screen, WHITE, (particulas[i].move(CENTRO)), 1)


running = True
while running:
    pygame.draw.circle(screen, WHITE, CENTRO, r0 + 2)  # borde blanco
    pygame.draw.circle(screen, BLACK, CENTRO, r0)      # agujero negro central

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Gravity point
    central_mass = pygame.draw.circle(screen, BLACK, CENTRO, r0)

    draw()

    pygame.display.update()