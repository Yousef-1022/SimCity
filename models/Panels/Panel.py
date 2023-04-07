import pygame
class Panel:
    def __init__(self,x,y,width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def display (self,screen,font_size,text_position,color, text, text_color):
        pygame.draw.rect(screen,color, (self.x,self.y, self.width, self.height))
        font = pygame.font.Font(None,font_size)
        text_surface = font.render(text, True,text_color)
        screen.blit(text_surface,text_position)