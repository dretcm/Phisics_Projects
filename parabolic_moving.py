import pygame
from pygame.locals import *
import math
import random

sin = lambda x: math.sin(x*math.pi/180)
cos = lambda x: math.cos(x*math.pi/180)
atan = lambda x: math.atan(x)*180/math.pi

pygame.init()

size = [1100, 700]
screen = pygame.display.set_mode(size)

done = True
clock = pygame.time.Clock()


v, angle = 0, 0
wind = -2
grav=-9.8
weight = 5
velocity = 100
radius = 20
floor_limit = size[1]
origin_x, origin_y = 10, floor_limit - 2*radius

font = pygame.font.Font(size=4)

V = lambda t, vx, vy, x, y: (x + vx*t, y - vy*t + 4.9*t**2, 3*t, vy-9.8*t, t+0.1)

class Bull():
    def __init__(self, v=20, x=origin_x, y=origin_y, angle=70, radius=radius, weight=1, air=False, grav=9.8):
        self.x = x
        self.y = y
        self.angle = angle
        self.t = 0.0
        self.radius = radius
        self.weight = weight
        self.W = self.weight * grav * 0.1
        self.air=air
        self.vx = v * cos(angle) * 0.1
        self.vy = v * sin(angle) * 0.1
        self.color = "blue"
        # Calculamos la resistencia del aire
        if air:
            self.color = "red"
            _v = pygame.math.Vector2(0,v)
            C_esfera = 0.47
            p_air = 1.225 * 0.1**4 # g/cm^3  # 1 pixels = 0.1 m
            A = radius**2 * math.pi
            self.air_resistance = 0.5 * C_esfera * p_air * A * pygame.math.Vector2.magnitude(_v) * pygame.math.Vector2.normalize(_v)

    def show(self, screen, floor_limit):
        if self.y+self.radius*2 < floor_limit:
            if self.air:
                self.W = self.W + self.air_resistance.y
                self.air = False

            self.vy = self.vy - self.W * self.t

            self.x = self.x + self.vx * self.t
            #self.y = int(self.y - self.vy * self.t + 0.5*self.W*self.t**2)
            self.y = self.y - self.vy*self.t
            self.t += 0.05

        pygame.draw.circle(screen, self.color, pygame.math.Vector2(self.x, self.y), self.radius)

        if self.y+self.radius*2 >= floor_limit:
            text = font.render(f"x={round(self.x*0.1,2)}", True, "black")
            screen.blit(text, [self.x-self.radius/2, self.y-self.radius/2])


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        # self.speed = wind#random.uniform(1, 3)  # Velocidad aleatoria
        self.direction = math.pi + random.uniform(-1, 1)  # Dirección aleatoria

    def move(self, wind):
        self.speed = -wind
        self.x += self.speed * 0.1 * math.cos(self.direction)
        self.y += self.speed * 0.1 * math.sin(self.direction)


particles = []

bulls = []
direction = False
grav_l = False
grav_r = False

rect_width = 100
rect_height = 60
rect_x = origin_x
rect_y = origin_y-50
x1 = rect_x - rect_width // 2
y1 = rect_y - rect_height // 2
x2 = rect_x + rect_width // 2
y2 = rect_y - rect_height // 2
x3 = rect_x + rect_width // 2
y3 = rect_y + rect_height // 2
x4 = rect_x - rect_width // 2
y4 = rect_y + rect_height // 2


def draw_rotated_rect(angle):
    angle_rad = math.radians(angle)

    x1_new = rect_x + math.cos(angle_rad) * (x1 - rect_x) - math.sin(angle_rad) * (y1 - rect_y)
    y1_new = rect_y - math.sin(angle_rad) * (x1 - rect_x) - math.cos(angle_rad) * (y1 - rect_y)
    x2_new = rect_x + math.cos(angle_rad) * (x2 - rect_x) - math.sin(angle_rad) * (y2 - rect_y)
    y2_new = rect_y - math.sin(angle_rad) * (x2 - rect_x) - math.cos(angle_rad) * (y2 - rect_y)
    x3_new = rect_x + math.cos(angle_rad) * (x3 - rect_x) - math.sin(angle_rad) * (y3 - rect_y)
    y3_new = rect_y - math.sin(angle_rad) * (x3 - rect_x) - math.cos(angle_rad) * (y3 - rect_y)
    x4_new = rect_x + math.cos(angle_rad) * (x4 - rect_x) - math.sin(angle_rad) * (y4 - rect_y)
    y4_new = rect_y - math.sin(angle_rad) * (x4 - rect_x) - math.cos(angle_rad) * (y4 - rect_y)


    pygame.draw.polygon(screen, [0, 0, 0], [(x1_new, y1_new), (x2_new, y2_new), (x3_new, y3_new), (x4_new, y4_new)])
    text = font.render(f"{angle}°", True, "white")
    screen.blit(text, [x2_new, y2_new])

font = pygame.font.Font('freesansbold.ttf', 32)

while done:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                direction = True
            if event.key == K_UP:
                velocity += 5
            if event.key == K_DOWN:
                velocity -= 5
            if event.key == K_RIGHT:
                grav_r = True
            if event.key == K_LEFT:
                grav_l = True                
            if event.key == K_w:
                weight += 1
            if event.key == K_s:
                weight -= 1
            if event.key == K_c:
                bulls = []           
        if event.type == KEYUP:
            if event.key == K_SPACE:
                direction = False
                x = rect_x + cos(v) * (x3 - rect_x) - sin(v) * (y3 - rect_y)
                y = rect_y - sin(v) * (x3 - rect_x)
                bulls.append(Bull(angle=angle, x=x, y=y, weight=weight, v=velocity, grav=-grav))
                bulls.append(Bull(angle=angle, x=x, y=y, weight=weight, v=velocity, air=True, grav=-grav))
                angle = 0
            if event.key == K_RIGHT:
                grav_r = False           
            if event.key == K_LEFT:
                grav_l = False

    screen.fill("skyblue")

    for _ in range(abs(wind)):
        particles.append(Particle(random.uniform(0, size[0] + 50), random.uniform(0, size[1] - 50)-10))

    aux = []
    for i in range(len(particles)):
        particles[i].move(wind)
        pygame.draw.circle(screen, particles[i].color, (int(particles[i].x), int(particles[i].y),), 2)
        if(particles[i].x > 0):
            aux.append(particles[i])
    particles = aux.copy()

    text = font.render(f"V={velocity* 0.1} m/s  g={round(grav,2)}m/s² Weight={weight}kg", True, "black")
    screen.blit(text, [10, 10])
    pygame.draw.line(screen, (60, 179, 113), [0, floor_limit], [size[0], floor_limit], 50)

    if direction:
        angle += 1
        v = angle
    if grav_r:
        grav += 0.1
    if grav_l:
        grav -= 0.1

    draw_rotated_rect(v)

    for i in range(len(bulls)):
        bulls[i].show(screen, floor_limit)

    pygame.display.flip()

pygame.quit()
