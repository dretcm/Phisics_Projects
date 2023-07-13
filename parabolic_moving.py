import pygame
from pygame.locals import *
import math

sin = lambda x: math.sin(x*math.pi/180)
cos = lambda x: math.cos(x*math.pi/180)
atan = lambda x: math.atan(x)*180/math.pi

pygame.init()

size = [1100, 700]
screen = pygame.display.set_mode(size)

done = True
clock = pygame.time.Clock()


v,angle = 0,0
radius = 20
floor_limit = 650
origin_x,origin_y=10,floor_limit - 2*radius

V = lambda t,vx,vy,x,y: (x + vx*t, y - vy*t + 4.9*t**2, 3*t, vy-9.8*t, t+0.1)

class Bull():
    def __init__(self, v=20,x=origin_x,y=origin_y, angle=70,radius=radius):
        self.x = x
        self.y = y
        self.vx = v*cos(angle)
        self.vy = v*sin(angle)
        self.angle = angle
        self.t = 0.0
        self.radius = radius

    def show(self, screen):
        self.x = self.x + self.vx*self.t
        self.y = self.y - self.vy*self.t + 4.9*self.t**2
        self.t += 0.1
        pygame.draw.circle(screen, "blue", [self.x, self.y], self.radius)


bulls = [] #[Bull(v=20,angle=80)]
velocity = False


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

while done:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                velocity = True
        if event.type == KEYUP:
            if event.key == K_SPACE:
                velocity = False
                print(angle)
                x = rect_x + cos(v) * (x3 - rect_x) - sin(v) * (y3 - rect_y)
                y = rect_y - sin(v) * (x3 - rect_x) #- cos(v) * (y3 - rect_y)
                bulls.append(Bull(angle=angle,x=x,y=y))
                angle = 0


    screen.fill("white")
    pygame.draw.line(screen, (60, 179, 113), [0, floor_limit], [size[0], floor_limit], 20)

    if velocity:
        angle += 1
        v= angle
    
    draw_rotated_rect(v)

    aux = []
    for i in range(len(bulls)):
        if bulls[i].y < floor_limit - radius:
            bulls[i].show(screen)
            aux.append(bulls[i])
    bulls = aux

    pygame.display.flip()

pygame.quit()