import pygame
from pytmx.util_pygame import load_pygame


# Map Size: 928 x 704
# See Tile:  29 x 22
# CantTile:  11 x 18

class Map:
    def __init__(self,screen,leftPanelWidth,topOrBottomPanelHeight):
        """Requires the screen, builderPanel width, and topOrBottomPanel height as parameters"""
        self.__screen = screen
        self.__map = load_pygame('./Map/TMX/befk_map.tmx')
        self.__panel_width = leftPanelWidth
        self.__panel_height = topOrBottomPanelHeight
        self.__scroll_x = 0
        self.__scroll_y = 0
        self.__objcount = 0
                
    def display(self):
        """Displays the map after initialization"""
        map_surface = pygame.Surface((self.__map.width * self.__map.tilewidth, self.__map.height * self.__map.tileheight))
        for layer in self.__map.visible_layers:
            if layer.name == "Objects":
                continue
            for x, y, gid in layer:
                tile = self.__map.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(tile,(x * self.__map.tilewidth, y * self.__map.tileheight))
                    #tile_rect = pygame.Rect(x * self.__map.tilewidth, y * self.__map.tileheight, self.__map.tilewidth, self.__map.tileheight)
                    #pygame.draw.rect(map_surface, (255, 255, 255), tile_rect, 1) #uncomment this to see the grid

        for obj in self.__map.objects:
            map_surface.blit(obj.image,(obj.x,obj.y))
            
        visible_surface = pygame.Surface((self.__screen.get_width() - self.__panel_width, self.__screen.get_height() - self.__panel_height))
        top_left = (self.__scroll_x, self.__scroll_y)

        # Copy the portion of the map that is visible into the visible surface, then draw the visible surface onto the screen
        visible_surface.blit(map_surface, (0, 0), pygame.Rect(top_left[0], top_left[1], visible_surface.get_width(), visible_surface.get_height()))
        self.__screen.blit(visible_surface, (self.__panel_width+1, self.__panel_height+1))

    def handleScroll(self,eventKey):
        """Scrolls the map when the players uses any arrow keys"""
        x , y = self.__scroll_x , self.__scroll_y
        noX = self.__map.width-(self.getActualMapWidth()//self.__map.tilewidth)     # Amount of x tiles which the screen does not render
        noY = self.__map.height-(self.getActualMapHeight()//self.__map.tileheight)  # Amount of y tiles which the screen does not render
        if eventKey == pygame.K_LEFT:
            x -= self.__map.tilewidth
            if(x>=0):
                self.__scroll_x = x
        elif eventKey == pygame.K_RIGHT:
            x += self.__map.tilewidth
            if(x<=(noX*self.__map.tilewidth)):
                self.__scroll_x = x
        elif eventKey == pygame.K_UP:
            y -= self.__map.tileheight
            if(y>=0):
                self.__scroll_y = y
        elif eventKey == pygame.K_DOWN:
            y += self.__map.tileheight
            if(y<=(noY*self.__map.tileheight)):
                self.__scroll_y = y
        else:
            pass
        
    def addObject(self,obj):
        """Addes an instantiated class into the list of objects"""
        objLayer = self.__map.get_layer_by_name("Objects")
        objLayer.append(obj)
        self.__objcount += 1
        
    def getClickedTile(self,mousePos):
        """Returns the map's actual tile coordinates"""
        builderPanelWidth = self.__panel_width
        descriptionPanelHeight = self.__panel_height
        pricePanelHeight = self.__panel_height
        if(not mousePos[0]<=builderPanelWidth \
            and not mousePos[1]<=descriptionPanelHeight \
            and not mousePos[1]>=(self.__screen.get_height()-pricePanelHeight)) :
            tile_x = (mousePos[0]-builderPanelWidth) // self.__map.tilewidth
            tile_y = (mousePos[1]-descriptionPanelHeight) // self.__map.tileheight
            map_tile_x = (self.__scroll_x // self.__map.tilewidth) + tile_x
            map_tile_y = (self.__scroll_y // self.__map.tileheight) + tile_y
            return (map_tile_x,map_tile_y)
        else:
            return (-1,-1)
    
    def getTileSetFromGid(self,tile_gid):
        return self.__map.get_tileset_from_gid(tile_gid)
    
    def getActualMapWidth(self):
        return self.__screen.get_width()-self.__panel_width
    
    def getActualMapHeight(self):
        return self.__screen.get_height()-(2*self.__panel_height)
    
    def returnMap(self):
        return self.__map
    
    def getNextObjId(self):
        return self.__map.nextobjectid
    
    def getStaticObjectByType(self,type):
        """Returns a TiledObject"""
        for o in self.__map.objects:
            if type == o.type:
                return o
            
    def getObjCount(self):
        return self.__objcount
    
    def getTileHeight(self):
        return self.__map.tileheight
    
    def getTileWidth(self):
        return self.__map.tilewidth
        