import pygame
from pygame.locals import *
import math

sin = lambda x: math.sin(x*math.pi/180)
cos = lambda x: math.cos(x*math.pi/180)

pygame.init()

size = [1100, 700]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


v = 10
angle = 0
x, y= 100, 600
increment_angle = 3

car_img = pygame.image.load('mycar.png')
car_rect = car_img.get_rect()

up = False
down = False
left = False
right = False

while 1:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_RIGHT:
                right = True
            if event.key == K_SPACE:
                x,y = size[0]//2, size[1]//2

        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_RIGHT:
                right = False

    screen.fill("white")

    if up:
        #print(angle,x,y)
        x -= v*sin(angle)
        y -= v*cos(angle)
    if down:
        x += v*sin(angle)
        y += v*cos(angle)

    if left:
        angle += increment_angle
    if right:
        angle -= increment_angle

    car_rect.center = (x,y)
    rotated_car = pygame.transform.rotate(car_img, angle)
    rotated_rect = rotated_car.get_rect(center=car_rect.center)
    screen.blit(rotated_car, rotated_rect)

    pygame.display.flip()

pygame.quit()