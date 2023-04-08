import pygame
import sys
from models.Map import Map
from models.Panels.BuilderPanel import BuilderPanel
from models.Panels.DescriptionPanel import DescriptionPanel
from models.Panels.Panel import Panel
from models.Panels.PricePanel import PricePanel

pygame.init()

# Game static variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_SPEED = 5
# Map
map = Map(SCREEN)
# Panels
description_panel = DescriptionPanel(0,0, SCREEN.get_width(), 32)
builder_panel = BuilderPanel(0,32,96,SCREEN.get_height() - 32)
price_panel = PricePanel(96, SCREEN.get_height() - 32, SCREEN.get_width() - 96, 32)
icon_filenames = ['./Map/Assets/Builder_assets/icon1.png'	, './Map/Assets/Builder_assets/icon2.png', './Map/Assets/Builder_assets/icon3.png', './Map/Assets/Builder_assets/icon4.png', './Map/Assets/Builder_assets/icon5.png', './Map/Assets/Builder_assets/icon6.png', './Map/Assets/Builder_assets/icon7.png']

def run():
    normal_cursor = True
    cursorImg = cursorImg = pygame.image.load('./Map/Assets/Builder_assets/icon1.png')
    cursorImgRect = cursorImg.get_rect()
    while True:
        cursorImgRect.center = pygame.mouse.get_pos()
        map.display()
        description_panel.display(SCREEN,24,(10,10),(128,128,128),"Funds: 2000 , more industrial zones needed",(255,255,255))
        price_panel.display(SCREEN,24,(96, SCREEN.get_height() - 20),(128,128,128),"$100 Road",(255,255,255))
        builder_panel.display(SCREEN,0,(0,0),(90,90,90),"",(0,0,0))
        builder_panel.display_assets(SCREEN,icon_filenames)

        for event in pygame.event.get(): # mouse button click, keyboard, or the x button.
            if pygame.mouse.get_pressed()[2]:
                normal_cursor = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if builder_panel.get_selected_icon_index(mouse_pos) != None:
                    cursorImgRect = cursorImg.get_rect()
                    cursorImg = pygame.image.load(icon_filenames[builder_panel.get_selected_icon_index(mouse_pos)])
                    cursorImgRect.center = mouse_pos
                    normal_cursor = False
            elif event.type == pygame.KEYDOWN:
                x = map.getScrollX()
                y = map.getScrollY()
                if event.key == pygame.K_LEFT:
                    x -= 32
                    if(x>=0):
                        map.updateScrollX(x)
                    elif event.key == pygame.K_RIGHT:
                        x += 32
                        if(x<=352):
                            map.updateScrollX(x)
                    elif event.key == pygame.K_UP:
                        y -= 32
                        if(y>=0):
                            map.updateScrollY(y)
                    elif event.key == pygame.K_DOWN:
                        y += 32
                        if(y<=576):
                            map.updateScrollY(y)
        if not normal_cursor:
            SCREEN.blit(cursorImg, cursorImgRect)

        pygame.display.update()
        SCREEN.fill((0, 0, 0))
