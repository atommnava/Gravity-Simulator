import math
import random
from math import cos, sin, sqrt
from random import randrange

import pygame

WIDTH = 1400
HEIGHT = 800
CENTER = WIDTH // 2, HEIGHT // 2
centerX = WIDTH // 2
centerY = HEIGHT // 2

# Agujero negro Campos
G = 1.2
M = 1e9

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Agujero negro
r0 = 25

pygame.init()


class Particle:
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




screen = pygame.display.set_mode((WIDTH, HEIGHT))

particles = []

r = 200


# Linea
""""
def generator():
    for i in range(1000):
        x = randrange(-500, 1000)
        y = 100
        p = Particle(x, y)
        particles.append(p)
"""

# Circulo
"""
def generator():
     for i in range(1000):
         ang = random.uniform(0, 1) * 2 * math.pi
         hyp = sqrt(random.uniform(0, 1)) * r
         adj = cos(ang) * hyp
         opp = sin(ang) * hyp
         x = centerX + adj
         y = centerY + opp
         p = Particle(x, y)
         particles.append(p)
"""

# Cuadrado
"""
def generator():
     for i in range(500):
         x = randrange(0, 500)
         y = randrange(0, 500)
         p = Particle(x, y)
         particles.append(p)
"""

# Flor
def generator():
    petals = 6
    for i in range(2):
        angle = random.uniform(0, 2 * math.pi)
        radius = 150 + 50 * math.sin(petals * angle)
        x = centerX + radius * cos(angle)
        y = centerY + radius * sin(angle)
        p = Particle(x, y)
        particles.append(p)

def generator_black_hole():
    for _ in range(25000):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(100, 250)
        x = centerX + radius * cos(angle)
        y = centerY + radius * sin(angle)
        p = Particle(x, y)
        # velocidad orbital pero incompleta (colapso eventual)
        speed = sqrt(G * M / radius) * 0.6  # 60% de la velocidad de escape
        p.momentum_x = -speed * sin(angle)
        p.momentum_y = speed * cos(angle)
        particles.append(p)


generator_black_hole()


def draw():
    for i in range(len(particles)):
        pygame.draw.circle(screen, WHITE, (particles[i].move(CENTER)), 1)


running = True
while running:
    pygame.draw.circle(screen, WHITE, CENTER, r0 + 2)  # borde blanco
    pygame.draw.circle(screen, BLACK, CENTER, r0)      # agujero negro central

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Gravity point
    central_mass = pygame.draw.circle(screen, BLACK, CENTER, r0)

    draw()

    pygame.display.update()