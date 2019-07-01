import pygame
import time
import random

WIDTH = 450
HEIGHT = 450
FPS = 30

pygame.init()
pygame.display.set_caption("Labirinto v1.0")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
