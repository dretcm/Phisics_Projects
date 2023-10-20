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


v,angle = 0,0
wind = -2
weigth=5
radius = 20
floor_limit = size[1]
origin_x,origin_y=10,floor_limit - 2*radius

V = lambda t,vx,vy,x,y: (x + vx*t, y - vy*t + 4.9*t**2, 3*t, vy-9.8*t, t+0.1)

class Bull():
    def __init__(self, v=20,x=origin_x,y=origin_y, angle=70,radius=radius,weigth=1,wind=-2):
        self.x = x
        self.y = y
        self.vx = v*cos(angle)
        self.vy = v*sin(angle)
        self.angle = angle
        self.t = 0.0
        self.radius = radius
        self.W = weigth * 9.8
        self.ax = wind*weigth #wind/(weigth if weigth!=0 else 0.0001) - 9.8 # resistencia/m = aceleración
        self.band=1
        self.weigth = weigth

    def show(self, screen,limit,wind):
        self.ax = wind*self.weigth #wind/(self.weigth if self.weigth!=0 else 0.0001) - 9.8 # resistencia/m = aceleración
        if self.y+self.radius<limit:
        	self.y = self.y - self.vy*self.t + 0.5*self.W*self.t**2
        else:
            if self.band:
                self.vx = 0
                self.band = 0
                self.t=0
            else:
                if self.weigth*0.3*9.8 < abs(self.ax):
                    self.vx = self.vx + self.ax*self.t
                    self.t += 0.1
                else:
                    self.t += 0.0

        self.x = self.x + self.vx*self.t + 0.5*self.ax*self.t**2
        if self.band:
            self.t += 0.1
        pygame.draw.circle(screen, "blue", [self.x, self.y], self.radius)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        #self.speed = wind#random.uniform(1, 3)  # Velocidad aleatoria
        self.direction = math.pi + random.uniform(-1,1)  # Dirección aleatoria

    def move(self,wind):
        self.speed = -wind
        self.x += self.speed * 0.1 * math.cos(self.direction)
        self.y += self.speed * 0.1 * math.sin(self.direction)



particles = []

bulls = [] #[Bull(v=20,angle=80)]
direction = False
velocity = 30


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
    
    pygame.draw.polygon(screen, [0,0,0], [(x1_new, y1_new), (x2_new, y2_new), (x3_new, y3_new), (x4_new, y4_new)])


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
                velocity += 1
            if event.key == K_DOWN:
                velocity -= 1
            if event.key == K_RIGHT:
                wind += 1
            if event.key == K_LEFT:
                wind -= 1
            if event.key == K_w:
                weigth+= 1
            if event.key == K_s:
                weigth -= 1
        if event.type == KEYUP:
            if event.key == K_SPACE:
                direction = False
                #print(angle)
                x = rect_x + cos(v) * (x3 - rect_x) - sin(v) * (y3 - rect_y)
                y = rect_y - sin(v) * (x3 - rect_x) #- cos(v) * (y3 - rect_y)
                bulls.append(Bull(angle=angle,x=x,y=y,weigth=weigth,v=velocity,wind=wind))
                angle = 0
                
    screen.fill("skyblue")

    for _ in range(abs(wind)):
        particles.append(Particle(random.uniform(0,size[0]+50), random.uniform(0,size[1]-50)-10))

    aux = []
    for i in range(len(particles)):
        particles[i].move(wind)
        pygame.draw.circle(screen, particles[i].color, (int(particles[i].x), int(particles[i].y),), 2)
        if(particles[i].x>0):
            aux.append(particles[i])
    particles = aux.copy()

    text = font.render(f"V={velocity} m/s  Wind={wind}m/s² Weigth={weigth}kg", True,"black")
    screen.blit(text, [10,10])
    pygame.draw.line(screen, (60, 179, 113), [0, floor_limit], [size[0], floor_limit], 50)

    if direction:
        angle += 1
        v= angle
    
    draw_rotated_rect(v)

    aux = []
    for i in range(len(bulls)):
        if bulls[i].x > 0:
            bulls[i].show(screen,floor_limit-radius,wind)
            aux.append(bulls[i])
    bulls = aux.copy()

    pygame.display.flip()

pygame.quit()
