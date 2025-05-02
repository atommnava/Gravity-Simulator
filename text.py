import math
import random
from math import cos, sin, sqrt
from random import randrange
import colorsys

import pygame

ANCHO = 1400
ALTURA = 800
CENTRO = ANCHO // 2, ALTURA // 2
centroX = ANCHO // 2
centroY = ALTURA // 2

def solve_gravity_ode(G, M, r0, v0, dt=0.01, steps=1000):
    r = r0
    v = v0
    results = []

    for _ in range(steps):
        a = -G * M / (r**2)
        v += a * dt
        r += v * dt
        results.append(r)
        if r <= 0:
            break  # colapsó al centro
    return results

# Solicitar valores al usuario
G = float(input("Ingresa el valor de G (constante gravitacional): "))
M = float(input("Ingresa el valor de M (masa del cuerpo central): "))
r0_ode = float(input("Ingresa el radio inicial (r0) en metros: "))
v0_ode = float(input("Ingresa la velocidad inicial (v0) en m/s: "))

print("\nResolvemos la ecuación diferencial para el movimiento radial...")

r_vals = solve_gravity_ode(G, M, r0_ode, v0_ode)
print(f"\nDistancias r(t) calculadas (primeros 10 pasos): {r_vals[:10]}")
print(f"\nÚltimo valor antes del colapso (si aplica): {r_vals[-1]:.4f} metros")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
        self.dt = 0.001  # Paso de tiempo pequeño para mayor precisión

    def move(self, x_y_central_mass):
        x2 = x_y_central_mass[0]
        y2 = x_y_central_mass[1]
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = math.atan2(y2 - self.y, x2 - self.x)
        force = (self.g * self.mass * M) / hyp
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)

        # Método de Euler para actualización de velocidad y posición
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
"""
def generator():
     for i in range(500):
         x = randrange(0, 500)
         y = randrange(0, 500)
         p = Particula(x, y)
         particulas.append(p)
"""

# Flor
def generator():
    petals = 6
    for i in range(2):
        angulo = random.uniform(0, 2 * math.pi)
        radio = 150 + 50 * math.sin(petals * angulo)
        x = centroX + radio * cos(angulo)
        y = centroY + radio * sin(angulo)
        p = Particula(x, y)
        particulas.append(p)

def agujero_negro_generador():
    for _ in range(25000):
        angulo = random.uniform(0, 2 * math.pi)
        radio = random.uniform(100, 250)
        x = centroX + radio * cos(angulo)
        y = centroY + radio * sin(angulo)
        p = Particula(x, y)
        # velocidad orbital pero incompleta (colapso eventual)
        speed = sqrt(G * M / radio) * 0.6  # 60% de la velocidad de escape
        p.momentum_x = -speed * sin(angulo)
        p.momentum_y = speed * cos(angulo)
        particulas.append(p)


agujero_negro_generador()


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