import pygame , sys
import pickle
from MenuClass import MenuClass
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.PricePanel import PricePanel
from models.zones.ResidentialZone import ResidentialZone
from models.zones.IndustrialZone import IndustrialZone
from models.zones.ServiceZone import ServiceZone
from models.PoliceDepartment import PoliceDepartment
from models.Stadium import Stadium
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
class_tobuild = ""
game_loop = True


def save_game(running, game_loop):
    # save the status of the game
    print("save")
    pass

def resume_game(running, game_loop):
    print("save")
    pass

def main_menu(running, game_loop):
    game_loop= False
    return game_loop

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
timer = Timer(game_speed, 200)
paused  = False

# Initialize grid system.
Grid = GridSystem(map)

def resume_game(running, game_loop):
    print("========================== resume ==================================")
    game_loop = True
    run(running, False)

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

    # load the parent back (since parent object is not serilizable and therfore cannot be pickled)
    print(list_of_tiled_objs)
    with open('game_state.pickle', 'wb') as f:
        pickle.dump(citizens, f)
        pickle.dump(list_of_tiled_objs, f)
    for i in range(len(list_of_tiled_objs)):
        list_of_tiled_objs[i]['parent'] = parents[i]

    game_loop = True
    run(running, False)

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

def run(running, loaded_game):
    normal_cursor = True
    cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer",icons))
    cursorImgRect = cursorImg.get_rect()
    day = timer.get_current_time().day
    month = timer.get_current_time().month
    TAX_VARIABLE = 0.05
    game_speed  = 1
    global game_loop

    # handle saved tiled objects
    if loaded_game:
        with open('game_state.pickle', 'rb') as f:
            loaded_citizens = pickle.load(f)
            loaded_objs = pickle.load(f)
        # Handle object creation
        for loaded_obj in loaded_objs:
            class_tobuild = loaded_obj['type']
            class_obj = globals().get(class_tobuild)
            obj = ""
            if class_obj is not None:
                if class_tobuild == "Road":
                    obj = class_obj(loaded_obj['x']//32,loaded_obj['y']//32,timer.get_current_date_str(),map)    # Change
                else:
                    obj = class_obj(loaded_obj['x']//32 - 1,loaded_obj['y']//32 - 1,timer.get_current_date_str(),map)    # Change
                map.addObject(obj.instance,player)
                class_tobuild = -1
            else:
                map.remove_obj(loaded_obj['x']//32,loaded_obj['y']//32,"Road")
            normal_cursor = True

    initial_citizens = []
    for i in range (1,11):
        c = Citizen()
        initial_citizens.append(c)
    game_loop = True

    while game_loop:
        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()

        description_panel.display(SCREEN,24,(10,10),(128,128,128),f"Funds: {player.money}$ , more industrial zones needed",(255,255,255))
        description_panel.displayTime(SCREEN,f"Time: {timer.get_current_date_str()}",(500,10))
        price_panel.display(SCREEN,24,(96, SCREEN.get_height() - 20),(128,128,128),"$100 Road",(255,255,255))
        builder_panel.display(SCREEN,0,(0,0),(90,90,90),"",(0,0,0))
        builder_panel.display_assets(SCREEN,icons)

        # Citizen adding Logic
        if (len(initial_citizens) != 0): # Initial edge case
            RZones = map.get_residential_zones()
            if(len(RZones) > 0):
                RZone = random.choice(RZones)
                for c in initial_citizens:
                    c.assign_to_residential_zone(RZone,map)
                    initial_citizens.remove(c)

        if(timer.get_current_time().month != month):
            RZones = map.get_residential_zones()
            if len(RZones) > 0:
                s = Citizen.get_current_satisfaction()
                curr_per = s*100/Citizen.get_max_possible_satisfaction()
                # Amount of citizens possible to be added depends on current overall satisfaction
                if (curr_per >= 25):
                    n = int(curr_per / 100 * 10)
                    for _ in range (n):
                        RZone = random.choice(RZones)
                        if RZone.properties['Capacity'] != len(RZone.properties['Citizens']):
                            c = Citizen()
                            c.assign_to_residential_zone(RZone,map)
                else:
                    # Random amount of sad citizens leave
                    lst = Citizen.get_sad_citizens(20)
                    if len(lst) > 0:
                        to_remove = random.randint(0, len(lst) - 1)
                        for i in range(to_remove):
                            lst[i].delete_citizen()
            month = timer.get_current_time().month



        # Zones and (Buildings,Roads) Expense Logic
        if(timer.get_current_time().day != day):
            for obj in map.get_all_objects():
                # Handle Buildings,Roads
                if obj.type == "Road" or obj.type == "PoliceDepartment" or obj.type == "Stadium":
                    if(has_year_passed_from_creation(obj,timer)):
                        player.money -= obj.properties['MaintenanceFee'] 
                else:
                    # Deduct MaintenanceFees for any Zone from Player
                    if(has_quarter_passed_from_creation(obj,timer)):
                        player.money -= obj.properties['MaintenanceFee']
                    # IncreaseRevenue of each WorkZone per day
                    total_citizens = len(obj.properties['Citizens'])
                    if(obj.type != "ResidentialZone" and total_citizens != 0):
                        obj.properties['Revenue'] += (MONEY_PER_DAY * total_citizens)
                    # Get revenue (TAX) from WorkZone to Player
                    elif(obj.type != "ResidentialZone" and has_year_passed_from_creation(obj,timer)):
                        revenue = obj.properties['Revenue'] * TAX_VARIABLE
                        player.money += revenue
                        obj.properties['Revenue'] = 0
            day = timer.get_current_time().day
            
            
        for event in pygame.event.get(): # mouse button click, keyboard, or the x button.
            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_loop = False
                show_menu(SCREEN, running, game_loop)
            elif event.type == pygame.MOUSEBUTTONUP:    # Cursor handling
                mouse_pos = pygame.mouse.get_pos()
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
                            if class_tobuild == "Road":
                                obj = class_obj(x,y,timer.get_current_date_str(),map)    # Change
                            else:
                                obj = class_obj(x - 1,y - 1,timer.get_current_date_str(),map)    # Change
                            map.addObject(obj.instance,player)
                            class_tobuild = -1
                        else:
                            map.remove_obj(x,y,"Road")
                            #print(f"Can't build class: {class_tobuild} because it doesn't exist")
                        normal_cursor = True
                if selected_icon != None:
                    # Handle cursor at selection
                    cursorImgRect = cursorImg.get_rect()
                    image_size = get_image_size(icons[selected_icon][1])
                    cursorImg = pygame.transform.scale(pygame.image.load(icons[selected_icon][0]), (image_size,image_size))
                    cursorImgRect.center = pygame.mouse.get_pos()
                    normal_cursor = False
                    class_tobuild = icons[selected_icon][1]
            elif event.type == pygame.KEYDOWN:  # Scroll handling
                map.handleScroll(event.key)
        

        if not normal_cursor:
            SCREEN.blit(cursorImg, cursorImgRect)
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
        # print(len(Citizen.get_all_citizens()))
