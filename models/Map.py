import pygame
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, screen):
        self.__screen = screen
        self.__map = load_pygame('./Map/TMX/befk_map.tmx')
        self.__panel_width = 96
        self.__panel_height = 32
        self.__scroll_x = 0
        self.__scroll_y = 0
        
    def scroll(self, dx, dy):
        # Update the scroll position by the specified amount
        self.__scroll_x += dx
        self.__scroll_y += dy
    
        # Constrain the scroll position to the bounds of the map
        self.__scroll_x = max(0, min(self.__scroll_x, self.__map.width * self.__map.tilewidth - self.__screen.get_width() + self.__panel_width))
        self.__scroll_y = max(0, min(self.__scroll_y, self.__map.height * self.__map.tileheight - self.__screen.get_height() + self.__panel_height))
            
    def display(self):
        map_surface = pygame.Surface((self.__map.width * self.__map.tilewidth, self.__map.height * self.__map.tileheight))
        for layer in self.__map.visible_layers:
            for x, y, gid in layer:
                tile = self.__map.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(tile,(x * self.__map.tilewidth, y * self.__map.tileheight))
                    #tile_rect = pygame.Rect(x * self.__map.tilewidth, y * self.__map.tileheight, self.__map.tilewidth, self.__map.tileheight)
                    #pygame.draw.rect(map_surface, (255, 255, 255), tile_rect, 1) #uncomment this to see the grid

        visible_surface = pygame.Surface((self.__screen.get_width() - self.__panel_width, self.__screen.get_height() - self.__panel_height))
        top_left = (self.__scroll_x, self.__scroll_y)

        # Copy the portion of the map that is visible into the visible surface
        visible_surface.blit(map_surface, (0, 0), pygame.Rect(top_left[0], top_left[1], visible_surface.get_width(), visible_surface.get_height()))

        # Draw the visible surface onto the screen
        self.__screen.blit(visible_surface, (self.__panel_width+1, self.__panel_height+1))
        
    def getTileWidth(self):
        return self.__map.tilewidth
    
    def getTileHeight(self):
        return self.__map.tileheight
    
    def getScrollX(self):
        return self.__scroll_x
    
    def getScrollY(self):
        return self.__scroll_y
    
    def updateScrollX(self,value):
        self.__scroll_x = value
        
    def updateScrollY(self,value):
        self.__scroll_y = value