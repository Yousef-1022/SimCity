import pygame
from models.Panels.Panel import Panel
class DescriptionPanel(Panel):
    def __init__(self,x,y,width, height):
        super().__init__(x,y,width,height)

    def displayTime(self,screen,time,text_position):
        font = pygame.font.Font(None,20)
        text_surface = font.render(time, True, (255, 255, 255))
        screen.blit(text_surface,text_position)