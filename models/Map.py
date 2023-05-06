import pygame
from pytmx.util_pygame import load_pygame


class Map:
    """
    Represents a game map.

    Attributes:
        __screen: The screen object where the map will be displayed.
        __map: The loaded TMX map.
        __panel_width: The width of the builder panel.
        __panel_height: The height of the top or bottom panel.
        __scroll_x: The horizontal scroll position of the map.
        __scroll_y: The vertical scroll position of the map.
        __objcount: The count of objects present in the map.

    Methods:
        __init__(self, screen, leftPanelWidth, topOrBottomPanelHeight): Initializes the Map object.
        display(self): Displays the map.
        handleScroll(self, eventKey): Handles map scrolling based on player input.
        addObject(self, obj, player): Adds an object to the map.
        getClickedTile(self, mousePos): Returns the coordinates of the clicked tile.
        getTileSetFromGid(self, tile_gid): Returns the tileset associated with the given GID.
        getActualMapWidth(self): Returns the actual width of the map.
        getActualMapHeight(self): Returns the actual height of the map.
        returnMap(self): Returns the TMX map object.
        getNextObjId(self): Returns the next object ID.
        getStaticObjectByType(self, type): Returns a TiledObject of the given type.
        getObjCount(self): Returns the count of objects in the map.
        getTileHeight(self): Returns the tile height.
        getTileWidth(self): Returns the tile width.
        collide_with_zone(self, zone1, zone2): Checks if two zones overlap.
        collide_with_water(self, obj_x_coord, obj_y_coord, obj_width, obj_height): Checks if an object collides with water.

    """

    def __init__(self, screen, leftPanelWidth, topOrBottomPanelHeight):
        """
        Initializes the Map object.

        Args:
            screen: The screen object where the map will be displayed.
            leftPanelWidth: The width of the builder panel.
            topOrBottomPanelHeight: The height of the top or bottom panel.
        """
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
            if layer.name == "Objects" or layer.name == "ObjectsTop":
                continue
            for x, y, gid in layer:
                tile = self.__map.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(tile,(x * self.__map.tilewidth, y * self.__map.tileheight))
                    tile_rect = pygame.Rect(x * self.__map.tilewidth, y * self.__map.tileheight, self.__map.tilewidth, self.__map.tileheight)
                    pygame.draw.rect(map_surface, (255, 255, 255), tile_rect, 1) #uncomment this to see the grid

        for obj in self.__map.objects:
            map_surface.blit(obj.image,(obj.x,obj.y))
            
        visible_surface = pygame.Surface((self.__screen.get_width() - self.__panel_width, self.__screen.get_height() - self.__panel_height))
        top_left = (self.__scroll_x, self.__scroll_y)

        # Copy the portion of the map that is visible into the visible surface, then draw the visible surface onto the screen
        visible_surface.blit(map_surface, (0, 0), pygame.Rect(top_left[0], top_left[1], visible_surface.get_width(), visible_surface.get_height()))
        self.__screen.blit(visible_surface, (self.__panel_width+1, self.__panel_height+1))

    def handleScroll(self,eventKey):
        """
        Scrolls the map when the player uses arrow keys.

        Args:
            eventKey: The key corresponding to the arrow key pressed.
        """
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
        
    def addObject(self, obj, player):
        """
        Adds an instantiated class into the list of objects.

        Args:
            obj: The object to be added.
            player: The player object is needed to add money.
        """
        can_be_added = True
        objLayer = self.__map.get_layer_by_name("Objects")

        if self.__objcount > 0:
            objects = self.get_all_objects()
        else:
            objects = []
        for ob in objects:
            if (self.collide_with_objects(ob, obj)):
                can_be_added = False
        if (obj.type != "Road" and self.collide_with_water(obj.x, obj.y, obj.width,obj.height)):
                can_be_added = False

        if can_be_added:
            player.money = player.money - int(obj.properties['Price'])
            objLayer.append(obj)
            self.__objcount += 1

    def remove_obj(self, x, y, obj_type):
        obj_layer = self.__map.get_layer_by_name("Objects")
        for obj in obj_layer:
            if (obj.x // 32)== x and (obj.y // 32) == y and obj.type == obj_type:
                obj_layer.remove(obj)
                self.__objcount-=1
                break

    def getClickedTile(self,mousePos):
        """
        Returns the map's actual tile coordinates based on the mouse position.

        Args:
            mousePos: The mouse position (x, y).

        Returns:
            The actual tile coordinates (map_tile_x, map_tile_y) or (-1, -1) if outside the map area.
        """
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
        """
        Returns the tileset associated with the given GID.

        Args:
            tile_gid: The GID of the tile.

        Returns:
            The tileset object associated with the GID.
        """
        return self.__map.get_tileset_from_gid(tile_gid)
    
    def getActualMapWidth(self):
        """
        Returns the actual width of the map.

        Returns:
            The actual width of the map.
        """
        return self.__screen.get_width()-self.__panel_width
    
    def getActualMapHeight(self):
        """
        Returns the actual height of the map.

        Returns:
            The actual height of the map.
        """
        return self.__screen.get_height()-(2*self.__panel_height)
    
    def returnMap(self):
        """
        Returns the TMX map object.

        Returns:
            The TMX map object.
        """
        return self.__map
    
    def getNextObjId(self):
        """
        Returns the next object ID.

        Returns:
            The next object ID.
        """
        return self.__map.nextobjectid
    
    def getStaticObjectByType(self,type):
        """
        Returns a TiledObject of the given type.

        Args:
            type: The type of the object.

        Returns:
            The TiledObject of the given type if found, otherwise None.
        """
        for o in self.__map.objects:
            if type == o.type:
                return o
            
    def getStaticObjectByName(self,name):
        """
        Returns a TiledObject of the given name.

        Args:
            name: The name of the object.

        Returns:
            The TiledObject of the given name if found, otherwise None.
        """
        for o in self.__map.objects:
            if name == o.name:
                return o
            
    def getObjCount(self):
        """
        Returns the count of objects in the map.

        Returns:
            The count of objects in the map.
        """
        return self.__objcount
    
    def getTileHeight(self):
        """
        Returns the tile height.

        Returns:
            The tile height.
        """
        return self.__map.tileheight
    
    def getTileWidth(self):
        """
        Returns the tile width.

        Returns:
            The tile width.
        """
        return self.__map.tilewidth
        
    def collide_with_objects(self,obj1, obj2):
        """
        Checks if two zones overlap.

        Args:
            obj1: The first  object.
            obj2: The second object.

        Returns:
            True if the zones overlap, False otherwise.
        """
        # Check if the zones overlap in the x-axis
        if (obj1.x < obj2.x + obj2.width) and (obj1.x + obj1.width > obj2.x):
            # Check if the zones overlap in the y-axis
            if (obj1.y < obj2.y + obj2.height) and (obj1.y + obj1.height > obj2.y):
                # The zones overlap
                return True
        
        # The zones don't overlap
        return False
    
    def collide_with_water(self, obj_x_coord, obj_y_coord, obj_width, obj_height):
        """
        Checks if an object collides with water or water edges.

        Args:
            obj_x_coord: The x-coordinate of the object's position.
            obj_y_coord: The y-coordinate of the object's position.
            obj_width: The width of the object.
            obj_height: The height of the object.

        Returns:
            True if collision detected with water or water edges, False otherwise.
        """
        for layer in self.__map.visible_layers:
            if layer.name == "Water" or layer.name == "WaterEdges":
                # Calculate the tile coordinates for the object's boundaries
                tile_x_start = int(obj_x_coord / self.__map.tilewidth)
                tile_x_end = int((obj_x_coord + obj_width) / self.__map.tilewidth)
                tile_y_start = int(obj_y_coord / self.__map.tileheight)
                tile_y_end = int((obj_y_coord + obj_height) / self.__map.tileheight)
                
                # Check if any tile within the object's boundaries is a water tile or water edges tile
                for y in range(tile_y_start, tile_y_end):
                    for x in range(tile_x_start, tile_x_end):
                        if layer.data[y][x] != 0:
                            # Collision detected with water or water edges
                            return True
        
        # No collision with water or water edges
        return False
        
    def get_all_objects(self):
        """
        Gets the list of all Dynamic objects in the map.

        Returns:
            A list of all Dynamic Tiled objects in the map. If no objects are present, an empty list is returned.
        """
        if self.__objcount == 0:
            return []
        else:
            res = []
            for obj in self.__map.objects:
                if obj.properties['Placeholder'] == "dynamic":
                    res.append(obj)
            return res

    def get_residential_zones(self):
        """
        Get the list of all the ResidentialZones
        
        Returns:
            A list of all Tiled objects representing ResidentialZones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() if obj.type == "ResidentialZone"]
        
    def get_work_zones(self):
        """
        Get the list of all the IndustrialZones and ServiceZones
        
        Returns:
            A list of all Tiled objects representing the IndustrialZones and ServiceZones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() \
                if obj.type == "IndustrialZone" or obj.type == "ServiceZone"]