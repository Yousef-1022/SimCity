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
        handle_scroll(self, eventKey): Handles map scrolling based on player input.
        add_object(self, obj, player): Adds an object to the map.
        get_clicked_tile(self, mousePos): Returns the coordinates of the clicked tile.
        get_tileset_from_gid(self, tile_gid): Returns the tileset associated with the given GID.
        get_actual_map_width(self): Returns the actual width of the map.
        get_actual_map_height(self): Returns the actual height of the map.
        return_map(self): Returns the TMX map object.
        get_next_obj_id(self): Returns the next object ID.
        get_static_object_by_type(self, type): Returns a TiledObject of the given type.
        get_object_count(self): Returns the count of objects in the map.
        get_tile_height(self): Returns the tile height.
        get_tile_width(self): Returns the tile width.
        collide_with_zone(self, zone1, zone2): Checks if two zones overlap.
        collide_with_water(self, obj_x_coord, obj_y_coord, obj_width, obj_height): Checks if an object collides with water.
        get_scroll_coordinates(self): Returns scroll_x and scroll_y in a list 

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
        
    
    def reinitialize(self, screen, leftPanelWidth, topOrBottomPanelHeight):
        """
        Reinitializes the Map object.

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
        map_surface = pygame.Surface(
            (self.__map.width * self.__map.tilewidth, self.__map.height * self.__map.tileheight))
        for layer in self.__map.visible_layers:
            if layer.name == "Objects" or layer.name == "ObjectsTop":
                continue
            for x, y, gid in layer:
                tile = self.__map.get_tile_image_by_gid(gid)
                if tile:
                    map_surface.blit(
                        tile, (x * self.__map.tilewidth, y * self.__map.tileheight))
                    #tile_rect = pygame.Rect(x * self.__map.tilewidth, y * self.__map.tileheight, self.__map.tilewidth, self.__map.tileheight)
                    #pygame.draw.rect(map_surface, (255, 255, 255), tile_rect, 1) #uncomment this to see the grid

        for obj in self.__map.objects:
            map_surface.blit(obj.image, (obj.x, obj.y))

        visible_surface = pygame.Surface((self.__screen.get_width(
        ) - self.__panel_width, self.__screen.get_height() - self.__panel_height))
        top_left = (self.__scroll_x, self.__scroll_y)

        # Copy the portion of the map that is visible into the visible surface, then draw the visible surface onto the screen
        visible_surface.blit(map_surface, (0, 0), pygame.Rect(
            top_left[0], top_left[1], visible_surface.get_width(), visible_surface.get_height()))
        self.__screen.blit(
            visible_surface, (self.__panel_width+1, self.__panel_height+1))

    def handle_scroll(self, eventKey):
        """
        Scrolls the map when the player uses arrow keys.

        Args:
            eventKey: The key corresponding to the arrow key pressed.
        """
        x, y = self.__scroll_x, self.__scroll_y
        # Amount of x tiles which the screen does not render
        noX = self.__map.width - \
            (self.get_actual_map_width()//self.__map.tilewidth)
        # Amount of y tiles which the screen does not render
        noY = self.__map.height - \
            (self.get_actual_map_height()//self.__map.tileheight)
        if eventKey == pygame.K_LEFT:
            x -= self.__map.tilewidth
            if (x >= 0):
                self.__scroll_x = x
        elif eventKey == pygame.K_RIGHT:
            x += self.__map.tilewidth
            if (x <= (noX*self.__map.tilewidth)):
                self.__scroll_x = x
        elif eventKey == pygame.K_UP:
            y -= self.__map.tileheight
            if (y >= 0):
                self.__scroll_y = y
        elif eventKey == pygame.K_DOWN:
            y += self.__map.tileheight
            if (y <= (noY*self.__map.tileheight)):
                self.__scroll_y = y
        else:
            pass

    def add_object(self, obj, player, init_tree=False, loaded_game=False):
        """
        Adds an instantiated class into the list of objects located on the Objects layer.

        Args:
            obj: The object to be added.
            player: The player object is needed to add money.
            init_tree: Optional boolean to indicate the creation of initial trees. Default: False
            loaded_game: Optional boolean to indicate that the game is loaded, the objCount and nextObj won't change. Default: False
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
        if (obj.type != "Road" and self.collide_with_water(obj.x, obj.y, obj.width, obj.height)):
            can_be_added = False

        if can_be_added:
            if (not init_tree):
                player.money = player.money - int(obj.properties['Price'])
            objLayer.append(obj)
            if (not loaded_game):
                self.__objcount += 1
                self.__map.nextobjectid += 1
        return obj

    def remove_road(self, x, y, obj_type, map):
        """
        Removes road if eligible
        
        Args:
        x: xTile coords
        y: yTile coords
        obj_type: Road Type
        """
        obj_layer = self.__map.get_layer_by_name("Objects")
        roads = self.get_all_roads()
        for obj in obj_layer:
            if (obj.x // (self.get_tile_width())) == x and (obj.y // (self.get_tile_height())) == y and obj.type == obj_type:
                connected_roads = get_all_connected_roads(obj, roads)
                connected_objects_temp = list(
                    set([ob for ob in get_all_neighboring_objects(connected_roads, map)]))
                connected_objects = []
                for ob in connected_objects_temp:
                    if ob.type == "ResidentialZone" or ob.type == "IndustrialZone" or "ServiceZone" == ob.type:
                        connected_objects.append(ob)
                R_zone = None
                for zone in connected_objects:
                    if zone.type == "ResidentialZone":
                        R_zone = zone
                if R_zone and len(connected_objects) <= 1 or not R_zone:
                    obj_layer.remove(obj)
                    self.__objcount-=1
                    del (obj)
                break

    def get_all_roads(self) -> list:
        """
        Returns a list consisting of all the roads created
        """
        objects = self.get_all_objects()
        return [obj for obj in objects if obj.type == "Road"]

    def get_clicked_tile(self, mousePos) -> tuple:
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
        if (not mousePos[0] <= builderPanelWidth
                and not mousePos[1] <= descriptionPanelHeight
                and not mousePos[1] >= (self.__screen.get_height()-pricePanelHeight)):
            tile_x = (mousePos[0]-builderPanelWidth) // self.__map.tilewidth
            tile_y = (
                mousePos[1]-descriptionPanelHeight) // self.__map.tileheight
            map_tile_x = (self.__scroll_x // self.__map.tilewidth) + tile_x
            map_tile_y = (self.__scroll_y // self.__map.tileheight) + tile_y
            return (map_tile_x, map_tile_y)
        else:
            return (-1, -1)

    def get_tileset_from_gid(self, tile_gid):
        """
        Returns the tileset associated with the given GID.

        Args:
            tile_gid: The GID of the tile.

        Returns:
            The tileset object associated with the GID.
        """
        return self.__map.get_tileset_from_gid(tile_gid)

    def get_actual_map_width(self):
        """
        Returns the actual width of the map.

        Returns:
            The actual width of the map.
        """
        return self.__screen.get_width()-self.__panel_width

    def get_actual_map_height(self):
        """
        Returns the actual height of the map.

        Returns:
            The actual height of the map.
        """
        return self.__screen.get_height()-(2*self.__panel_height)

    def return_map(self):
        """
        Returns the TMX map object.

        Returns:
            The TMX map object.
        """
        return self.__map

    def get_next_obj_id(self):
        """
        Increases the Map.tmx internal object counter
        
        When the function is called, the counter is increased

        Returns:
            The next object ID.
        """
        return self.__map.nextobjectid

    def set_next_obj_id(self, id):
        """
        Sets the map's TileMap nextobjectidid attribute to the given Id
        
        Usecase:
        Loading the game 
        """
        self.__map.nextobjectid = id

    def set_obj_count(self, cnt):
        """
        Sets the map's objcount attribute to the given Id
        
        Usecase:
        Loading game 
        """
        self.__objcount = cnt
        
    def set_scrollers(self,scrollers : list):
        """
        Sets the map's scroll_x and scroll_y attributes
        """
        self.__scroll_x = scrollers[0]
        self.__scroll_y = scrollers[1]

    def get_static_object_by_type(self, type):
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

    def get_static_object_by_name(self, name):
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

    def get_object_count(self):
        """
        Returns the count of objects in the map.

        Returns:
            The count of objects in the map.
        """
        return self.__objcount

    def get_tile_height(self):
        """
        Returns the tile height.

        Returns:
            The tile height.
        """
        return self.__map.tileheight

    def get_tile_width(self):
        """
        Returns the tile width.

        Returns:
            The tile width.
        """
        return self.__map.tilewidth

    def collide_with_objects(self, obj1, obj2):
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
                tile_x_end = int((obj_x_coord + obj_width) /
                                 self.__map.tilewidth)
                tile_y_start = int(obj_y_coord / self.__map.tileheight)
                tile_y_end = int((obj_y_coord + obj_height) /
                                 self.__map.tileheight)

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
            return [obj for obj in self.get_all_objects()
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

    def get_zone_by_id(self, id):
        """
        Returns a Zone based on the given id
        """
        for obj in self.get_all_objects():
            if obj.id == id:
                return obj
        return None

    def add_building(self, building):
        """
        Function used to append the Building object onto the ObjectsTop layer.
        Usecase: after reconstructing the building dictionary, it can be used to append directly to the map
        
        Args:
        bulding: TiledMap object
        """
        objLayer = self.__map.get_layer_by_name("ObjectsTop")
        objLayer.append(building)
        
    def create_button(self, font, text, text_padding, prompt_x, prompt_y, prompt_width, prompt_height,
    button_width, button_height, p_m=1, b_m=2):
        """
        Function used to create a clickable button
        
        Args:
        font: pygame.font.Font
        text: String to be on button
        text_padding: int showing the padding required for the text
        prompt_x: mouse_x - prompt_width // 2 value
        prompt_y: mouse_y - prompt_height // 2
        prompt_width: int showing pixel size of prompt width
        prompt_height: int showing pixel size of prompt height
        p_m: optional padding multipler to move button location
        b_m: optional button multipler to move button location
        
        Returns:
        a button (rectangle)
        """
        button_x = prompt_x + (prompt_width - button_width) // 2
        button_y = prompt_y + prompt_height + text_padding * p_m - button_height * b_m
        button = pygame.draw.rect(self.__screen, (100, 100, 100), (button_x, button_y, button_width, button_height))
        button_text = font.render(text, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.__screen.blit(button_text, button_text_rect)
        return button
    
    def draw_prompt(self, pos, zone) -> list:
        """
        Draws a prompt on the screen when clicking with the right mouse button
        
        Args:
        pos: mouse_pos
        zone: Zone TiledObject
        
        Returns:
        List of two buttons (rectangle) which can be used to be clicked on for either upgrade or demolish/remove
        """
        mouse_x, mouse_y = pos[0], pos[1]
        prompt_width, prompt_height = 180, 180
        prompt_x = mouse_x - prompt_width // 2
        prompt_y = mouse_y - prompt_height // 2
        pygame.draw.rect(self.__screen, (220, 220, 220),
                         (prompt_x, prompt_y, prompt_width, prompt_height))
        pygame.draw.rect(self.__screen, (150, 150, 150),
                         (prompt_x, prompt_y, prompt_width, prompt_height), 2)
        font = pygame.font.Font(None, 24)
        line_height = font.get_linesize()
        text_padding = 10
        
        can_classify = False
        can_upgrade = False
        
        if zone.type[-4:] == 'Zone':    
            amount_citizens = len(zone.properties['Citizens'])
            amount_buildings = len(zone.properties['Buildings'])

            if amount_citizens == 0 and amount_buildings == 0:
                sat = 0.0
                can_classify = True
            else:
                sat = (sum(c.satisfaction for c in zone.properties['Citizens']) / amount_citizens) if amount_citizens != 0 else 0.0
                sat = '{:.2f}'.format(round(sat, 2))
                can_upgrade = True

            lines = [
                f"Saturation: {amount_citizens}",
                f"Satisfaction: {sat}",
                f"Capacity: {zone.properties['Capacity']}",
                f"Level: {zone.properties['Level']}"
            ]
        else:
            lines = [
                f"Cost: {zone.properties['Price']}",
                f"MaintenanceFee: {zone.properties['MaintenanceFee']}",
                f"Date: {zone.properties['CreationDate']}",
                f"Radius: {zone.properties['Radius']} tiles",
                f"SatAdd: {zone.properties['Satisfaction'] * 100}% ",
            ]
            
        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(
                prompt_x + prompt_width // 2, prompt_y + line_height * (i + 1) + text_padding))
            self.__screen.blit(text, text_rect)

        res = []
        
        if zone.type[-4:] != 'Zone':
            remove_btn = self.create_button(font,"Remove",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,150,30)
            res.append(remove_btn)
            
        elif can_upgrade and zone.properties['Level'] < 3 and amount_citizens > 0:
            upgrade_btn = self.create_button(font,"Upgrade",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,150,30,1,3)
            res.append(upgrade_btn)
            demolish_btn = self.create_button(font,"Demolish",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,150,30,2)
            res.append(demolish_btn)

        elif can_classify:
            classfy_btn = self.create_button(font,"Reclassify",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,150,30)
            res.append(classfy_btn)
        
        else:
            demolish_btn = self.create_button(font,"Demolish",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,150,30)
            res.append(demolish_btn)
            
        return res
        
    def does_obj_exist(self,object) -> bool:
        """
        Checks if the given object on the object layer exists
        """
        if (object in self.get_all_objects()):
            return True
        return False
    
    def draw_confirm_prompt_to_demolish(self,pos,zone):
        """
        Draws a prompt on the screen after clicking on the demolish button
        Used to demolish a Zone
        
        Returns:
        a button (rectangle) which can be used to be clicked to demolish the zone
        """
        mouse_x, mouse_y = pos[0], pos[1]
        prompt_width, prompt_height = 150, 150
        prompt_x = mouse_x - prompt_width // 2
        prompt_y = mouse_y - prompt_height // 2
        pygame.draw.rect(self.__screen, (220, 220, 220),
                         (prompt_x, prompt_y, prompt_width, prompt_height))
        pygame.draw.rect(self.__screen, (150, 150, 150),
                         (prompt_x, prompt_y, prompt_width, prompt_height), 2)
        font = pygame.font.Font(None, 24)
        line_height = font.get_linesize()
        text_padding = 10
        lines = [
            f"{zone.name}",
            f"Citizens: {len(zone.properties['Citizens'])}",
            f"{zone.properties['CreationDate']}",
            f"Are you sure?",
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(prompt_x + prompt_width // 2, prompt_y + line_height * (i + 1) + text_padding))
            self.__screen.blit(text, text_rect) 
        
        btn = self.create_button(font,"Demolish!",text_padding,prompt_x,prompt_y,prompt_width,prompt_height,100,30)
        return btn  
    
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
                if (obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount -= 1
                    handle_satisfaction_zone_removal(
                        obj, self.get_residential_zones())
            elif obj.type == 'Road':
                obj_layer = self.__map.get_layer_by_name("Objects")
                if (obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount -= 1
            elif (len(obj.properties['Citizens']) == 0):
                obj_layer = self.__map.get_layer_by_name("Objects")
                if (obj in obj_layer):
                    obj_layer.remove(obj)
                    self.__objcount-=1
            del (obj)
        except Exception as e:
            print(f"Fatal error to reclassify {obj}. Error: {e}")

    def remove_disaster_or_building(self, db):
        """
        Function used to delete the given disaster or building which is on the ObjectsTop layer
        
        Use case: destory disasters or buildings
        
        Args: 
        building: TiledObject existing on the ObjectsTop layer
        """
        obj_layer = self.__map.get_layer_by_name("ObjectsTop")
        obj_layer.remove(db)
        del (db)
    
    def get_yet_to_occupy_homes(self) -> list:
        """
        Function used to get the ResidentialZones which have free capacity to add a Citizen into
        
        Returns:
        list of ResidentialZones with citizens less than its capacity
        """
        return [RZone for RZone in self.get_residential_zones() if
                  len(RZone.properties['Citizens']) < RZone.properties['Capacity']]
        
    def get_service_zones(self):
        """
        Get service zones
        
        Returns:
            service zones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects()
                    if obj.type == "ServiceZone"]

    def get_industrial_zones(self):
        """
        # Get Industrial zones
        
        Returns:
            service zones
        """
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects()
                    if obj.type == "IndustrialZone"]

    def get_roads(self):
        if self.__objcount == 0:
            return []
        else:
            return [obj for obj in self.get_all_objects()
                    if obj.type == "Road"]

    def add_disaster_to_map(self, disaster):
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
    
    def get_scroll_coordinates(self) -> list:
        """
        Returns the Scroll handling variables
        """
        return [self.__scroll_x,self.__scroll_y]
