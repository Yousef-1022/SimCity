import pygame
import sys
import pickle
from models.Map import Map
from models.BuildingAdder import *
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.PricePanel import PricePanel
from models.TaxAllocator import TaskAllocator
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
from models.Citizen import Citizen
import random

pygame.init()

# Game static variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_SPEED = 5
MONEY_PER_DAY = 20
allocated_tax = 0.05

# Map & Panels
description_panel = DescriptionPanel(0, 0, SCREEN.get_width(), 32)
builder_panel = BuilderPanel(0, 32, 96, SCREEN.get_height() - 32)
price_panel = PricePanel(96, SCREEN.get_height() - 32,
                         SCREEN.get_width() - 96, 32)
icons_dir = "./Map/Assets/Builder_assets/"
icons = [get_icon_and_type(f, icons_dir)
         for f in get_files_from_dir(icons_dir)]
map = Map(SCREEN, builder_panel.get_width(), description_panel.get_height())
global class_tobuild
game_loop = True

# Game simulation variables
player = Player("HUMAN", 100000)
game_speed = 1
game_speed_multiplier = [100, 200, 300]
chosen_speed = 1
timer = Timer(game_speed, game_speed_multiplier[chosen_speed])
paused = False


def run(running, loaded_game, flag, tax):
    global list_of_tiled_objs, saved_game_speed, saved_speed_multiplier, saved_current_time_str
    allocated_tax = tax
    normal_cursor = True
    cursorImg = pygame.image.load(get_icon_loc_by_name("bulldozer", icons))
    cursorImgRect = cursorImg.get_rect()
    game_speed = 1
    global game_loop
    class_tobuild = ""
    # handle saved tiled objects
    initial_citizens = []
    if loaded_game:
        with open('game_state.pickle', 'rb') as f:
            loaded_citizens = pickle.load(f)
            loaded_objs = pickle.load(f)
            loaded_timer = pickle.load(f)
            loaded_objCount = pickle.load(f)
            loaded_nextObjCount = pickle.load(f)
            loaded_tax = pickle.load(f)
            map.set_next_obj_id(loaded_nextObjCount)
            map.set_obj_count(loaded_objCount)

        # Handle object creation
        for loaded_obj in loaded_objs:
            class_tobuild = loaded_obj['type']
            class_obj = globals().get(class_tobuild)
            obj = ""
            if class_obj is not None:
                obj = class_obj(loaded_obj['x']//32, loaded_obj['y'] //
                                32, timer.get_current_date_str(), map)    # Change
                obj.instance.properties['CreationDate'] = loaded_obj['properties']['CreationDate']
                if (loaded_obj['type'][-4:] == 'Zone'):
                    obj.instance.properties['Level'] = loaded_obj['properties']['Level']
                    obj.instance.properties['Capacity'] = loaded_obj['properties']['Capacity']
                    obj.instance.properties['MaintenanceFee'] = loaded_obj['properties']['MaintenanceFee']
                    obj.instance.properties['Revenue'] = loaded_obj['properties']['Revenue']
                elif (loaded_obj['type'] == "Forest"):
                    obj.instance.properties['Year'] = loaded_obj['properties']['Year']
                    obj.instance.properties['Mature'] = loaded_obj['properties']['Mature']
                obj.instance.id = loaded_obj['id']
                map.add_object(obj.instance, player, False, True)
                class_tobuild = -1
            else:
                map.remove_obj(loaded_obj['x']//32,
                               loaded_obj['y']//32, "Road")
            normal_cursor = True
            if loaded_obj['type'][-4:] == 'Zone':
                for building in loaded_obj['properties']['Buildings']:
                    b = create_building(building, map)
                    obj_layer = map.return_map().get_layer_by_name("ObjectsTop")
                    obj_layer.append(b)
                    obj.instance.properties['Buildings'].append(b.__dict__)

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
        timer.game_speed = loaded_timer[0]
        timer.game_speed_multiplier = loaded_timer[1]
        timer.current_time = timer.get_timer_from_str(loaded_timer[2])
        allocated_tax = loaded_tax

    day = timer.get_current_time().day
    month = timer.get_current_time().month
    game_start_time = timer.get_current_date_str()
    if not loaded_game and flag:
        flag = False
        initial_citizens = []
        for i in range(1, 11):
            c = Citizen()
            initial_citizens.append(c)
        randomize_initial_forests(map, player, timer)
    game_loop = True


    clicked_cords = None
    clicked_zone = None
    upgrade = None
    reclassify = None
    demolish = None
    demolish_confirm = None
    
    held_price = 0
    class_tobuild = "Nothing"
    randomizer_for_disaster = False
    while game_loop:

        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()

        description_panel.display(SCREEN, 24, (10, 10), (128, 128, 128),
                                  f"Funds: ${player.money}        Citizens: {get_total_citizens()}      Tax: {allocated_tax}", (0, 0, 0))
        description_panel.display_time(
            SCREEN, f"Time: {timer.get_current_date_str()}", (400, 10))
        description_panel.display_game_speed(
            SCREEN, timer, game_speed_multiplier)
        price_panel.display(SCREEN, 24, (102, SCREEN.get_height(
        ) - 20), (128, 128, 128), f'${(held_price)} for {class_tobuild}', (0, 0, 0))
        builder_panel.display(SCREEN, 0, (0, 0), (90, 90, 90), "", (0, 0, 0))
        builder_panel.display_assets(SCREEN, icons)

        # Citizen adding Logic
        if (len(initial_citizens) != 0):  # Initial edge case
            if len(map.get_residential_zones()) != 0:
                first_R_Zone = map.get_residential_zones()[0]
                for c in initial_citizens:
                    assign_to_residential_zone(c, first_R_Zone, map)
                    handle_citizen_addition_satisfaction(c, map)
                    initial_citizens.remove(c)

        if (timer.get_current_time().month != month):
            add_citizens_to_game(map)
            for zone in map.get_residential_zones():
                assign_zone_citizens_to_work(zone, map)
            if (player.money <= 0):
                humans = Citizen.get_all_citizens()
                for key in humans:
                    res = humans[key].satisfaction - \
                        (humans[key].satisfaction * 0.35)
                    if (res <= 0):
                        humans[key].satisfaction = 0.0
                    else:
                        humans[key].satisfaction = res
            month = timer.get_current_time().month

        # Zones and (Buildings,Roads,Forest) Expense Logic
        if (timer.get_current_time().day != day):
            for obj in map.get_all_objects():
                did_a_quarter_pass = has_quarter_passed_from_creation(
                    obj, timer)
                did_a_year_pass = has_year_passed_from_creation(obj, timer)

                # Handle ServiceBuildings,Roads Expense
                if obj.type == "Road" or obj.type == "PoliceDepartment" or obj.type == "Stadium":
                    if (did_a_year_pass):
                        player.money -= obj.properties['MaintenanceFee']

                # Handle Forest Expense and Grow
                elif obj.type == "Forest":
                    if (did_a_year_pass):
                        randomizer_for_disaster = has_random_years_passed_from_start(
                            game_start_time, timer)
                        if obj.properties['Mature']:
                            player.money -= obj.properties['MaintenanceFee']
                        else:
                            obj.properties['Year'] += 1
                            obj.properties['Satisfaction'] += 0.03
                            handle_tree_growth(map,obj)
                            if obj.properties['Year'] == 10:
                                obj.properties['Mature'] = True
                # Handle Zones Expense
                else:
                    # Deduct MaintenanceFees for any Zone from Player
                    if (did_a_quarter_pass):
                        player.money -= obj.properties['MaintenanceFee']
                    # IncreaseRevenue of each WorkZone per day
                    total_citizens = len(obj.properties['Citizens'])
                    if (obj.type != "ResidentialZone" and total_citizens != 0):
                        obj.properties['Revenue'] += (
                            MONEY_PER_DAY * total_citizens)
                    # Get revenue (TAX) from WorkZone to Player
                    elif (obj.type != "ResidentialZone" and did_a_year_pass):
                        revenue = obj.properties['Revenue'] * allocated_tax
                        player.money += revenue
                        obj.properties['Revenue'] = 0
            day = timer.get_current_time().day

        for event in pygame.event.get():  # mouse button click, keyboard, or the x button.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                description_panel.handle_game_speed_click(
                    event, timer, game_speed_multiplier)

            mouse_pos = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
                clicked_zone = upgrade = reclassify = demolish = None
                clicked_cords = mouse_pos
                class_tobuild = "Nothing"
                held_price = 0

            if pygame.mouse.get_pressed()[0]:
                if reclassify:
                    if reclassify.collidepoint(mouse_pos):
                        map.reclassify_zone(clicked_zone)
                        player.money += (float(clicked_zone.properties["Price"])*0.5)
                    clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                if upgrade:
                    if upgrade.collidepoint(mouse_pos):
                        upgrade_zone(clicked_zone,map)
                        player.money -= ((float(clicked_zone.properties["Price"])*0.5) * (clicked_zone.properties["Level"]+0.25))
                        clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                    elif demolish.collidepoint(mouse_pos):
                        demolish_confirm = map.draw_confirm_prompt_to_demolish(mouse_pos,clicked_zone)
                        upgrade = reclassify = demolish = None
                    else:
                        clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                if demolish:
                    if demolish.collidepoint(mouse_pos):
                        demolish_confirm = map.draw_confirm_prompt_to_demolish(mouse_pos,clicked_zone)
                        upgrade = reclassify = demolish = None
                    else:
                        clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                if demolish_confirm:
                    if demolish_confirm.collidepoint(mouse_pos):
                        demolish_zone(clicked_zone,map,player)
                        clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_loop = False
                show_menu(SCREEN,map, running, game_loop, run, allocated_tax, list_of_tiled_objs,
                          saved_game_speed, saved_speed_multiplier, saved_current_time_str)
            elif event.type == pygame.MOUSEBUTTONUP:    # Cursor handling
                selected_icon = builder_panel.get_selected_icon_index(
                    mouse_pos)
                if (not normal_cursor):
                    x, y = map.get_clicked_tile(mouse_pos)
                    if x == -1 or y == -1:
                        normal_cursor = True
                    else:
                        # Handle object creation
                        class_obj = globals().get(class_tobuild)
                        obj = ""
                        if class_obj is not None:
                            disaster_make = None
                            if class_tobuild == "Road":
                                obj = class_obj(
                                    x, y, timer.get_current_date_str(), map)
                            elif class_tobuild == "Disaster":
                                disaster_make = Disaster(
                                    x-1, y-1, timer.get_current_date_str(), map)
                                obj = disaster_make.instance
                                zones = map.get_all_objects()
                                to_destory = []
                                for p in get_area(obj):
                                    tmp = tile_in_which_zone(p, zones)
                                    if (tmp):
                                        if (tmp not in to_destory):
                                            to_destory.append(tmp)
                                obj.properties['linked_objs'] = to_destory
                                map.add_disaster_to_map(obj)
                            else:
                                obj = class_obj(
                                    x - 1, y - 1, timer.get_current_date_str(), map)

                            if (not disaster_make):
                                instance = map.add_object(obj.instance, player)
                                # Satisfaction handling for: Forest, Stadium, and PoliceDepartment
                                if (is_satisfaction_zone(instance)):
                                    handle_satisfaction_zone_addition(
                                        map, instance)
                            class_tobuild = "Nothing"
                            held_price = 0
                        else:
                            map.remove_road(x, y, "Road", map)
                        normal_cursor = True
                if selected_icon != None:
                    # Handle cursor at selection
                    cursorImgRect = cursorImg.get_rect()
                    image_size = get_image_size(icons[selected_icon][1])
                    cursorImg = pygame.transform.scale(pygame.image.load(
                        icons[selected_icon][0]), (image_size, image_size))
                    cursorImgRect.center = pygame.mouse.get_pos()
                    normal_cursor = False
                    class_tobuild = icons[selected_icon][1]
                    the_class = globals().get(class_tobuild)
                    if (the_class):
                        held_price = the_class.price
                    else:
                        held_price = 0
            elif event.type == pygame.KEYDOWN:  # Scroll handling
                clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
                map.handle_scroll(event.key)

        if not normal_cursor:
            clicked_cords = clicked_zone = upgrade = reclassify = demolish = demolish_confirm = None
            SCREEN.blit(cursorImg, cursorImgRect)
        
        clicked_cords,clicked_zone,upgrade,reclassify,demolish,demolish_confirm = handle_prompt(map,clicked_cords,clicked_zone,upgrade,reclassify,demolish,demolish_confirm)
        handle_disaster_logic(map,timer)
        handle_disaster_random_logic(map,timer.get_current_date_str(),randomizer_for_disaster)


        # Limit the frame rate to 60 FPS
        timer.update_time(paused)
        timer.tick(60)

        pygame.display.update()
        SCREEN.fill((0, 0, 0))
        saved_game_speed = timer.game_speed
        saved_speed_multiplier = timer.game_speed_multiplier
        saved_current_time_str = timer.get_current_date_str()

        list_of_tiled_objs = []
        for obj in map.get_all_objects():
            x = obj
            my_dict = x.__dict__
            list_of_tiled_objs.append(my_dict)
