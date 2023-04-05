import pygame
import sys

pygame.init()

# Game static variables
SCREEN_WIDTH = pygame.display.Info().current_w - 60
SCREEN_HEIGHT = pygame.display.Info().current_h - 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
