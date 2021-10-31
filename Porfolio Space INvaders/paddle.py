import pygame
from pygame.locals import *


class Paddle():

    def __init__(self, screen):
        # Create Pad
        self.screen = screen
        self.y = 610
        self.x = 385
        self.paddle = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.x, self.y, 50, 50))
        self.bullet = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(1000, 1000, 0, 0))
        self.bullet_x_pos = 635
        self.bullets = []
        self.bullet_mov = 10
        pygame.display.flip()


    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_a] and self.x > 15:
            print("a")
            self.x -= 30
        if key[pygame.K_d] and self.x < 770:
            print("d")
            self.x += 30
        if key[pygame.K_SPACE]:
            print("Space pressed")
            self.bullet = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.x+25, self.y, 5, 20))
            self.bullets.append(self.bullet)
            pygame.display.flip()


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.x, self.y, 50, 50))
        for bullet in self.bullets:
            bullet = pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.bullet_x_pos, 500, 5, 20))
        pygame.display.update()
