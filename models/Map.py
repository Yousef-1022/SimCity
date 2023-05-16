import pygame
from pytmx.util_pygame import load_pygame
from models.Utils import *

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
        
    def addObject(self, obj, player,init_tree=False):
        """
        Adds an instantiated class into the list of objects located on the Objects layer.

        Args:
            obj: The object to be added.
            player: The player object is needed to add money.
            init_tree: Optional boolean value to indicate the creation of initial trees
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
            # if obj.type == "Road":
            if (not init_tree):
                player.money = player.money - int(obj.properties['Price'])
            objLayer.append(obj)
            self.__objcount += 1
        return obj
    
    def remove_road(self, x, y, obj_type, map):
        obj_layer = self.__map.get_layer_by_name("Objects")
        roads = self.get_all_roads()
        for obj in obj_layer:
            if (obj.x // 32)== x and (obj.y // 32) == y and obj.type == obj_type:
                # connected_roads = get_all_connected_roads(obj, roads) # SHOULD BE ADDED LATER
                # if(len(get_neighboring_objects(connected_roads, map))) <= 1:
                obj_layer.remove(obj)
                self.__objcount-=1
                break
            # else:
            #     print("Can't demolish a road because it connects objects!!")

    def get_all_roads(self):
        objects =  self.__map.get_layer_by_name("Objects")     
        return [obj for obj in objects if obj.type == "Road"]
    
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
        Gets the list of all Dynamic objects located on the Objects layer of the map.

        Returns:
            A list of all Dynamic Tiled objects in the map. If no objects are present, an empty list is returned.
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.__map.get_layer_by_name("Objects") if obj.properties['Placeholder'] == 'dynamic']
        
    def get_buildings(self):
        """
        Gets the list of all buildings which get created on top of the Zones.
        These buildings are extracted from the ObjectsTop layer of the map.
        
        Returns:
            A list of all Tiled Objects located on the ObjectsTop layer of the map, if no objects are present,
            an empty list is returned.
        """
        return [obj for obj in self.__map.get_layer_by_name("ObjectsTop") if obj.properties['Placeholder'] == 'dynamic']

    # def set_all_objects(self, objs):


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
            
    def get_satisfaction_increasers(self) -> list:
        """
        Gets the Objects which can affect the Citizens satisfaction, eg: Stadium,PoliceDepartment, and Forest

        Args:
        map: TiledMap object

        Returns:
        a List full of Dynamic TiledObjects 
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() if obj.type == "Stadium" or obj.type == "PoliceDepartment" or obj.type == "Forest"]
        
    def get_zone_by_id(self,id):
        """
        Returns a Zone based on the given id
        """
        for obj in self.get_all_objects():
            if obj.id == id:
                return obj
        return None
    
    def add_building(self,building):
        """
        Function used to append the Building object onto the ObjectsTop layer.
        Usecase: after reconstructing the building dictionary, it can be used to append directly to the map
        
        Args:
        bulding: TiledMap object
        """
        objLayer = self.__map.get_layer_by_name("ObjectsTop")
        objLayer.append(building)
        
    def draw_prompt(self, pos, zone):
        """
        Draws a prompt on the screen when clicking with the right mouse button
        
        Returns:
        a button (rectangle) which can be used to be clicked
        """
        mouse_x, mouse_y = pos[0], pos[1]
        prompt_width, prompt_height = 180, 180
        prompt_x = mouse_x - prompt_width // 2
        prompt_y = mouse_y - prompt_height // 2
        pygame.draw.rect(self.__screen, (220, 220, 220), (prompt_x, prompt_y, prompt_width, prompt_height))
        pygame.draw.rect(self.__screen, (150, 150, 150), (prompt_x, prompt_y, prompt_width, prompt_height), 2)
        font = pygame.font.Font(None, 24)
        line_height = font.get_linesize()
        text_padding = 10

        amount_citizens = len(zone.properties['Citizens'])
        can_classify = False
        
        if amount_citizens == 0:
            sat = 0.0
            can_classify = True
        else:
            sat = sum(c.satisfaction for c in zone.properties['Citizens']) / amount_citizens
            sat = '{:.2f}'.format(round(sat, 2))
            can_classify = False
            
        lines = [
            f"Saturation: {amount_citizens}",
            f"Satisfaction: {sat}",
            f"Capacity: {zone.properties['Capacity']}",
            f"Level: {zone.properties['Level']}"
        ]

        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(prompt_x + prompt_width // 2, prompt_y + line_height * (i + 1) + text_padding))
            self.__screen.blit(text, text_rect)

        res = None
        
        if zone.properties['Level'] < 3 and amount_citizens > 0:
            button_width, button_height = 150, 30
            button_x = prompt_x + (prompt_width - button_width) // 2
            button_y = prompt_y + prompt_height + text_padding - button_height*2
            button = pygame.draw.rect(self.__screen, (100, 100, 100), (button_x, button_y, button_width, button_height))
            button_text = font.render("Upgrade", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.__screen.blit(button_text, button_text_rect)
            res = button

        elif can_classify:
            button_width, button_height = 150, 30
            button_x = prompt_x + (prompt_width - button_width) // 2
            button_y = prompt_y + prompt_height + text_padding - button_height*2
            button = pygame.draw.rect(self.__screen, (100, 100, 100), (button_x, button_y, button_width, button_height))
            button_text = font.render("Reclassify", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.__screen.blit(button_text, button_text_rect)
            res = button

        return res
    
    def draw_prompt_to_delete(self, pos, zone):
        """
        Draws a prompt on the screen when clicking with the right mouse button
        Used to delete PoliceDepartment or Stadium
        
        Returns:
        a button (rectangle) which can be used to be clicked to delete the zone
        """
        mouse_x, mouse_y = pos[0], pos[1]
        prompt_width, prompt_height = 180, 180
        prompt_x = mouse_x - prompt_width // 2
        prompt_y = mouse_y - prompt_height // 2
        pygame.draw.rect(self.__screen, (220, 220, 220), (prompt_x, prompt_y, prompt_width, prompt_height))
        pygame.draw.rect(self.__screen, (150, 150, 150), (prompt_x, prompt_y, prompt_width, prompt_height), 2)
        font = pygame.font.Font(None, 24)
        line_height = font.get_linesize()
        text_padding = 10
        
        lines = [
            f"Cost: {zone.properties['Price']}",
            f"MaintenanceFee: {zone.properties['MaintenanceFee']}",
            f"Date: {zone.properties['CreationDate']}",
            f"Radius: {zone.properties['Radius']} tiles",
            f"SatAdd: {zone.properties['Satisfaction'] * 100}% ",
        ]
        
        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(prompt_x + prompt_width // 2, prompt_y + line_height * (i + 1) + text_padding))
            self.__screen.blit(text, text_rect)
            
        button_width, button_height = 150, 30
        button_x = prompt_x + (prompt_width - button_width) // 2
        button_y = prompt_y + prompt_height + text_padding - button_height*2
        button = pygame.draw.rect(self.__screen, (100, 100, 100), (button_x, button_y, button_width, button_height))
        button_text = font.render("Remove", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.__screen.blit(button_text, button_text_rect)
        return button


    def reclassify_zone(self,obj):
        """
        Reclassifies the zone if it does not have any citizens
        
        Can be used to delete a PoliceDepartment, Stadium, Forest, Road
        
        Args:
        zone: TiledObj representing the object to reclassify
        """
        try:
            if (obj.type == 'PoliceDepartment' or obj.type == 'Stadium' or obj.type == 'Forest'):
                obj_layer = self.__map.get_layer_by_name("Objects")
                if(obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount-=1
                    handle_satisfaction_zone_removal(obj,self.get_residential_zones())
            elif obj.type == 'Road':
                obj_layer = self.__map.get_layer_by_name("Objects")
                if(obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount-=1
            elif (len(obj.properties['Citizens']) == 0):
                obj_layer = self.__map.get_layer_by_name("Objects")
                if(obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount-=1
        except Exception as e:
            print(f"Fatal error to reclassify {obj}. Error: {e}")
            
    def remove_disaster_or_building(self,db):
        """
        Function used to delete the given disaster or building which is on the ObjectsTop layer
        
        Use case: destory disasters or buildings
        
        Args: 
        building: TiledObject existing on the ObjectsTop layer
        """
        obj_layer = self.__map.get_layer_by_name("ObjectsTop")
        obj_layer.remove(db)
    
    def get_service_zones(self):
        """
        Get service zones
        
        Returns:
            service zones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() \
                if  obj.type == "ServiceZone"]
        
    def get_insustrial_zones(self):
        """
        # Get Industrial zones
        
        Returns:
            service zones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() \
                if  obj.type == "IndustrialZone"]
        
    def get_roads(self):
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects() \
                if  obj.type == "Road"] 
            
    def add_disaster_to_map(self,disaster):
        """
        Adds the Disaster onto the ObjectsTop layer of the map
        
        Args:
        disaster: TiledObj representing a Disaster
        """
        objLayer = self.__map.get_layer_by_name("ObjectsTop")
        objLayer.append(disaster)
        
    def get_all_disasters(self) -> list:
        """
        Returns all active disasters currently happening
        """
        return [obj for obj in self.__map.get_layer_by_name("ObjectsTop") if obj.type == 'Disaster' and obj.properties['Placeholder'] == 'dynamic']