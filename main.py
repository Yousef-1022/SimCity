import pygame , sys
import pickle
from models.Map import Map
from models.BuildingAdder import *
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.PricePanel import PricePanel
from models.zones.ResidentialZone import ResidentialZone
from models.zones.IndustrialZone import IndustrialZone
from models.zones.ServiceZone import ServiceZone
from models.PoliceDepartment import PoliceDepartment
from models.Stadium import Stadium
from models.Forest import Forest
from models.Disaster import Disaster
from models.Player import Player
from models.Timer import Timer
from models.Utils import *
from models.Road import Road
from models.GridSystem import GridSystem
from models.Citizen import Citizen
import random

pygame.init()

# Game static variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_SPEED = 5
MONEY_PER_DAY = 20
TAX_VARIABLE = 0.05

# Map & Panels
description_panel = DescriptionPanel(0,0, SCREEN.get_width(), 32)
builder_panel = BuilderPanel(0,32,96,SCREEN.get_height() - 32)
price_panel = PricePanel(96, SCREEN.get_height() - 32, SCREEN.get_width() - 96, 32)
icons_dir = "./Map/Assets/Builder_assets/"
icons = [get_icon_and_type(f,icons_dir) for f in get_files_from_dir(icons_dir)]
map = Map(SCREEN, builder_panel.getWidth(), description_panel.getHeight())
global class_tobuild
game_loop = True


def show_menu(screen, running, game_loop):
    menu_height = 400
    menu_width = 400
    screen_width = 1024
    screen_height = 768
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2

    menu_surface = pygame.Surface((menu_width, menu_height))
    menu_surface.fill((200, 200, 200))
    # Create the menu options
    menu_options = [
        ("Resume Game", resume_game),
        ("Save Game", save_game),
        ("Main menu", main_menu)
    ]

    # Add the menu options to the menu surface
    font = pygame.font.SysFont("Calibri", 48, bold=True)
    selected_option = 0
    menu_loop = True
    while menu_loop:
        for i, (text, action) in enumerate(menu_options):
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(menu_width / 2, 75 + i * 75))
            if i == selected_option:
                pygame.draw.rect(menu_surface, (220, 220, 220), text_rect, 2)
            else:
                pygame.draw.rect(menu_surface, (180, 180, 180), text_rect, 2)
            menu_surface.blit(text_surface, text_rect)

        # Show the menu surface on the main surface
        screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.update()

# Game simulation variables
player = Player("HUMAN", 100000)
game_speed  = 1
game_speed_multiplier = [100,200,300]
chosen_speed = 1
timer = Timer(game_speed, game_speed_multiplier[chosen_speed])
paused  = False

# Initialize grid system.
Grid = GridSystem(map)

def resume_game(running, game_loop):
    print("========================== resume ==================================")
    game_loop = True
    run(running, False, False)

def save_game(running, game_loop):
    print("========================== save ==================================")
    citizens = []
    citizens_objs = Citizen.get_all_citizens()
    for citizen_id, citizen in citizens_objs.items():
        citizen_list = []
        citizen_list.append(citizen_id)
        if citizen.home:
            citizen_list.append(citizen.home.id)
        else:
            citizen_list.append(-1)
        if citizen.work:
            citizen_list.append(citizen.work.id)
        else:
            citizen_list.append(-1)
        citizen_list.append(citizen.satisfaction)
        citizens.append(citizen_list)

    parents = []
    # update tiled_object list
    for obj in list_of_tiled_objs:
        obj['properties']['Citizens'] = []
        parents.append(obj['parent'])
        obj['parent'] = ""
        if obj['type'][-4:] == 'Zone':
            for building in obj['properties']['Buildings']:
                building['parent'] = ""

    #print(list_of_tiled_objs)
    # load the parent back (since parent object is not serilizable and therfore cannot be pickled)
    with open('game_state.pickle', 'wb') as f:
        pickle.dump(citizens, f)
        pickle.dump(list_of_tiled_objs, f)
    for i in range(len(list_of_tiled_objs)):
        list_of_tiled_objs[i]['parent'] = parents[i]
        if list_of_tiled_objs[i]['type'][-4:] == 'Zone':
            for building in list_of_tiled_objs[i]['properties']['Buildings']:
                building['parent'] = map.returnMap()

    game_loop = True
    run(running, False, False)

def main_menu(running, game_loop):
    print("========================== Main menu ==================================")
    game_loop= False
    # return game_loop

def show_menu(screen, running, game_loop):
    menu_height = 400
    menu_width = 400
    screen_width = 1024
    screen_height = 768
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2

    menu_surface = pygame.Surface((menu_width, menu_height))
    menu_surface.fill((200, 200, 200))
    # Create the menu options
    menu_options = [
        ("Resume Game", resume_game),
        ("Save Game", save_game),
        ("Main menu", main_menu)
    ]

    # Add the menu options to the menu surface
    font = pygame.font.SysFont("Calibri", 48, bold=True)
    selected_option = 0
    menu_loop = True
    while menu_loop:
        for i, (text, action) in enumerate(menu_options):
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(menu_width / 2, 75 + i * 75))
            if i == selected_option:
                pygame.draw.rect(menu_surface, (220, 220, 220), text_rect, 2)
            else:
                pygame.draw.rect(menu_surface, (180, 180, 180), text_rect, 2)
            menu_surface.blit(text_surface, text_rect)

        # Show the menu surface on the main surface
        screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    selected_option = max(0, selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    selected_option = min(len(menu_options) - 1, selected_option + 1)
                elif event.key == pygame.K_RETURN:
                    action = menu_options[selected_option][1]
                    game_loop = action(running, game_loop)
                    menu_loop = False

def handle_satisfaction_zone_addition(SZone:TiledObject):
    """
    After the player creates a Stadium, PoliceDepartment, or Forest, it checks nearby Citizens and adds satisfaction
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone,SZone) <= SZone.properties['Radius']):
            if (SZone.type == "Forest"):
                if(is_there_a_blocker_between(SZone,RZone,map.get_all_objects())):
                    continue
                else:
                    for c in RZone.properties['Citizens']:
                        tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                        if tmp <= 100:
                            c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            else:
                for c in RZone.properties['Citizens']:
                    tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                    if tmp <= 100:
                        c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
                    
def handle_tree_growth(SZone:TiledObject):
    """
    After the tree grows, it must affect the nearby citizens
    """
    for RZone in map.get_residential_zones():
        if (distance_between_two(RZone,SZone) <= SZone.properties['Radius']):
            if(is_there_a_blocker_between(SZone,RZone,map.get_all_objects())):
                continue
            else:
                for c in RZone.properties['Citizens']:
                    tmp = c.satisfaction + (SZone.properties['Satisfaction']*c.satisfaction) 
                    if tmp <= 100:
                        c.satisfaction += (SZone.properties['Satisfaction']*c.satisfaction)
            

def handle_prompt(clckd_crds,clckd_zn,upgrd,rclssfy):
    """
    Handles prompt when viewing the information of the Zone
    """
    if clckd_crds:
        if (clckd_zn):
            # Handle deletion of PoliceDepartment or Stadium
            if(clckd_zn.type == "PoliceDepartment" or clckd_zn.type == "Stadium"):
                upgrd = None
                rclssfy = map.draw_prompt_to_delete(clckd_crds,clckd_zn)
            else:
                # Handle already clicked Zone (RZone,CZone,IZone)
                if(clckd_zn.properties['Level'] <= 3):
                    btn = map.draw_prompt(clckd_crds,clckd_zn)
                    if (len(clckd_zn.properties['Citizens']) == 0):
                        upgrd = None
                        rclssfy = btn
                    else:
                        upgrd = btn
                        rclssfy = None
                else:
                    upgrd = rclssfy = None
        else:
            # Reterive the Zone if not clicked in the first place
            zones = [obj for obj in map.get_all_objects() if (obj.type != "Forest" and obj.type != "Road")]
            clckd_zn = tile_in_which_zone(map.getClickedTile(clckd_crds),zones)
            if (clckd_zn):
                # Handle deletion of PoliceDepartment or Stadium
                if(clckd_zn.type == "PoliceDepartment" or clckd_zn.type == "Stadium"):
                    upgrd = None
                    rclssfy = map.draw_prompt_to_delete(clckd_crds,clckd_zn)
                else:
                    # Handle already clicked Zone (RZone,CZone,IZone)
                    if(clckd_zn.properties['Level'] <= 3):
                        btn = map.draw_prompt(clckd_crds,clckd_zn)
                        if (len(clckd_zn.properties['Citizens']) == 0):
                            upgrd = None
                            rclssfy = btn
                        else:
                            upgrd = btn
                            rclssfy = None
                    else:
                        upgrd = rclssfy = None
    return clckd_crds, clckd_zn, upgrd, rclssfy

def randomize_initial_forests():
    """
    Creates random forests at the start of the game
    """
    coords = [(11,5),(28,33),(6,16),(32,23)]
    num_choices = random.randint(1, len(coords))
    to_insert = random.sample(coords, num_choices)
    for p in to_insert:
        frst = Forest(p[0],p[1],timer.get_current_date_str(),map)
        map.addObject(frst.instance,player,True)  
    
def run(running, loaded_game, flag):
    normal_cursor = True
    cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer",icons))
    cursorImgRect = cursorImg.get_rect()
    day = timer.get_current_time().day
    month = timer.get_current_time().month
    game_start_time = timer.get_current_date_str()
    TAX_VARIABLE = 0.05
    # game_speed  = 1
    global game_loop
    class_tobuild = ""
    # handle saved tiled objects
    initial_citizens = []
    if loaded_game:
        with open('game_state.pickle', 'rb') as f:
            loaded_citizens = pickle.load(f)
            loaded_objs = pickle.load(f)
        #print(loaded_citizens)
        # Handle object creation
        for loaded_obj in loaded_objs:
            class_tobuild = loaded_obj['type']
            class_obj = globals().get(class_tobuild)
            obj = ""
            if class_obj is not None:
                obj = class_obj(loaded_obj['x']//32,loaded_obj['y']//32 ,timer.get_current_date_str(),map)    # Change
                if (loaded_obj['type'][-4:] == 'Zone'):
                    obj.instance.properties['Level'] = loaded_obj['properties']['Level']
                    obj.instance.properties['Capacity'] = loaded_obj['properties']['Capacity']
                    obj.instance.properties['MaintenanceFee'] = loaded_obj['properties']['MaintenanceFee']
                    obj.instance.properties['CreationDate'] = loaded_obj['properties']['CreationDate']
                    obj.instance.properties['Revenue'] = loaded_obj['properties']['Revenue']
                map.addObject(obj.instance,player)
                class_tobuild = -1
            else:
                map.remove_obj(loaded_obj['x']//32,loaded_obj['y']//32,"Road")
            normal_cursor = True
            if loaded_obj['type'][-4:] == 'Zone':
                for building in loaded_obj['properties']['Buildings']:
                    #print(loaded_obj['name'],"THE NAME <-- GOES TO BUILDING",loaded_obj['properties']['Buildings'])
                    b = create_building(building, map)
                    obj_layer = map.returnMap().get_layer_by_name("ObjectsTop")
                    obj_layer.append(b)

        # handle citizens restore
        for loaded_citizen in loaded_citizens:
            # citizen
            c = Citizen()
            # handle home zone
            if loaded_citizen[1] != -1:
                home_zone = map.get_zone_by_id(loaded_citizen[1])
                if home_zone:
                    home_zone.properties['Citizens'].append(c)
                    c.home = home_zone
            # handle work zone
            if loaded_citizen[2] != -1:
                work_zone = map.get_zone_by_id(loaded_citizen[2])
                if work_zone:
                    work_zone.properties['Citizens'].append(c)
                    c.work = work_zone
            c.satisfaction = loaded_citizen[3]
    if not loaded_game and flag:
        flag = False
        initial_citizens = []
        for i in range (1,11):
            c = Citizen()
            initial_citizens.append(c)
        randomize_initial_forests()
    game_loop = True

    
    clicked_cords = None
    clicked_zone = None
    upgrade = None
    reclassify = None
    held_price = 0
    class_tobuild = "Nothing"
    randomizer_for_disaster = False    
    while game_loop:
        
        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()

        description_panel.display(SCREEN,24,(10,10),(128,128,128),f"Funds: ${player.money} , Citizens: {get_total_citizens()}",(255,255,255))
        description_panel.displayTime(SCREEN,f"Time: {timer.get_current_date_str()}",(500,10))
        description_panel.display_game_speed(SCREEN, timer, game_speed_multiplier)
        price_panel.display(SCREEN,24,(96, SCREEN.get_height() - 20),(128,128,128),f'${(held_price)} for {class_tobuild}',(255,255,255))
        builder_panel.display(SCREEN,0,(0,0),(90,90,90),"",(0,0,0))
        builder_panel.display_assets(SCREEN,icons)

        # Citizen adding Logic
        if (len(initial_citizens) != 0): # Initial edge case
            if len (map.get_residential_zones()) != 0:
                first_R_Zone = map.get_residential_zones()[0]
                for c in initial_citizens:
                    assign_to_residential_zone(c,first_R_Zone,map)
                    handle_citizen_addition_satisfaction(c,map)
                    initial_citizens.remove(c)

        if(timer.get_current_time().month != month):   
            add_citizens_to_game(map)
            for zone in map.get_residential_zones():
                assign_zone_citizens_to_work(zone, map)
            month = timer.get_current_time().month
        
        
        # Zones and (Buildings,Roads,Forest) Expense Logic 
        if(timer.get_current_time().day != day):
            for obj in map.get_all_objects():
                did_a_quarter_pass = has_quarter_passed_from_creation(obj,timer)
                did_a_year_pass = has_year_passed_from_creation(obj,timer)
                
                # Handle ServiceBuildings,Roads Expense
                if obj.type == "Road" or obj.type == "PoliceDepartment" or obj.type == "Stadium":
                    if(did_a_year_pass):
                        player.money -= obj.properties['MaintenanceFee']
                        
                # Handle Forest Expense and Grow
                elif obj.type == "Forest":
                    if(did_a_year_pass):
                        randomizer_for_disaster = has_random_years_passed_from_start(game_start_time,timer)
                        if obj.properties['Mature']:
                            player.money -= obj.properties['MaintenanceFee']
                        else:
                            obj.properties['Year'] += 1
                            obj.properties['Satisfaction'] += 0.03
                            handle_tree_growth(obj)
                            if obj.properties['Year'] == 10:
                                obj.properties['Mature'] = True
                # Handle Zones Expense
                else:
                    # Deduct MaintenanceFees for any Zone from Player
                    if(did_a_quarter_pass):
                        player.money -= obj.properties['MaintenanceFee']
                    # IncreaseRevenue of each WorkZone per day
                    total_citizens = len(obj.properties['Citizens'])
                    if(obj.type != "ResidentialZone" and total_citizens != 0):
                        obj.properties['Revenue'] += (MONEY_PER_DAY * total_citizens)
                    # Get revenue (TAX) from WorkZone to Player
                    elif(obj.type != "ResidentialZone" and did_a_year_pass):
                        revenue = obj.properties['Revenue'] * TAX_VARIABLE
                        player.money += revenue
                        obj.properties['Revenue'] = 0
            day = timer.get_current_time().day
            
            
        for event in pygame.event.get(): # mouse button click, keyboard, or the x button.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                description_panel.handle_game_speed_click(event, timer, game_speed_multiplier)

            mouse_pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
                clicked_zone = upgrade = reclassify = None
                clicked_cords = mouse_pos
                class_tobuild = "Nothing"
                held_price = 0
                
            if pygame.mouse.get_pressed()[0]:
                if reclassify:
                    if reclassify.collidepoint(mouse_pos):
                        map.reclassify_zone(clicked_zone)
                        player.money += (float(clicked_zone.properties["Price"])*0.5)
                        clicked_cords = clicked_zone = upgrade = reclassify = None
                if upgrade:
                    if upgrade.collidepoint(mouse_pos):
                        upgrade_zone(clicked_zone,map)
                        player.money -= ((float(clicked_zone.properties["Price"])*0.5) * (clicked_zone.properties["Level"]+0.25))
                clicked_cords = clicked_zone = upgrade = reclassify = None

            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_loop = False
                show_menu(SCREEN, running, game_loop)
            elif event.type == pygame.MOUSEBUTTONUP:    # Cursor handling
                selected_icon = builder_panel.get_selected_icon_index(mouse_pos) 
                if (not normal_cursor):
                    x,y = map.getClickedTile(mouse_pos)
                    if  x == -1 or y == -1: 
                        normal_cursor= True 
                    else:
                        # Handle object creation
                        class_obj = globals().get(class_tobuild)
                        obj = ""
                        if class_obj is not None:
                            disaster_make = None
                            if class_tobuild == "Road":
                                obj = class_obj(x,y,timer.get_current_date_str(),map)
                            elif class_tobuild == "Disaster":
                                disaster_make = Disaster(x-1,y-1,timer.get_current_date_str(),map)
                                obj = disaster_make.instance
                                zones = map.get_all_objects()
                                to_destory = []
                                for p in get_area(obj):
                                    tmp = tile_in_which_zone(p,zones)
                                    if(tmp):
                                        if (tmp not in to_destory):
                                            to_destory.append(tmp)
                                obj.properties['linked_objs'] = to_destory
                                map.add_disaster_to_map(obj)
                            else:
                                obj = class_obj(x - 1,y - 1,timer.get_current_date_str(),map)

                            if (not disaster_make):
                                instance = map.addObject(obj.instance,player)
                                # Satisfaction handling for: Forest, Stadium, and PoliceDepartment
                                if(is_satisfaction_zone(instance)):
                                    handle_satisfaction_zone_addition(instance)
                            class_tobuild = "Nothing"
                            held_price = 0
                        else:
                            map.remove_road(x,y,"Road", map)
                        normal_cursor = True
                if selected_icon != None:
                    # Handle cursor at selection
                    cursorImgRect = cursorImg.get_rect()
                    image_size = get_image_size(icons[selected_icon][1])
                    cursorImg = pygame.transform.scale(pygame.image.load(icons[selected_icon][0]), (image_size,image_size))
                    cursorImgRect.center = pygame.mouse.get_pos()
                    normal_cursor = False
                    class_tobuild = icons[selected_icon][1]
                    the_class = globals().get(class_tobuild)
                    if (the_class):
                        held_price = the_class.price
                    else:
                        held_price = 0 
            elif event.type == pygame.KEYDOWN:  # Scroll handling
                clicked_cords = clicked_zone = upgrade = reclassify = None
                map.handleScroll(event.key)
        

        if not normal_cursor:
            clicked_cords = clicked_zone = upgrade = reclassify = None
            SCREEN.blit(cursorImg, cursorImgRect)
        
        clicked_cords,clicked_zone,upgrade,reclassify = handle_prompt(clicked_cords,clicked_zone,upgrade,reclassify)
        handle_disaster_logic(map,timer)
        handle_disaster_random_logic(map,timer.get_current_date_str(),randomizer_for_disaster)

                
        # Limit the frame rate to 60 FPS
        timer.update_time(paused)
        timer.tick(60)

        pygame.display.update()
        SCREEN.fill((0, 0, 0))
        global list_of_tiled_objs
        list_of_tiled_objs = []
        for obj in map.get_all_objects(): 
            x = obj
            my_dict = x.__dict__
            list_of_tiled_objs.append(my_dict)
