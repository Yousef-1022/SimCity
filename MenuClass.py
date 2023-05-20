import pygame
import main
import pickle
from models.TaxAllocator import TaskAllocator


class MenuClass:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("My Game")

        # Set up fonts
        self.instruction_font = pygame.font.Font(None, 20)
        self.menu_font = pygame.font.Font(None, 40)
        self.selected_font = pygame.font.Font(None, 60)

        # Set up colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.selected_color = (0, 0, 0)

        # Set up options
        self.menu_options = [
            ("New Game", False),
            ("Options", False),
            ("Load Game", False),
            ("Exit", False),
        ]

        self.options_options = [
            ("Resume", False),
            ("Instructions", False),
            ("Save", False),
            ("Main Menu", False),
        ]

        self.instruction_text = ["First, select a game speed to start the game with.",
                                 "Next, zone areas for residential, commercial\n, and industrial development.",
                                 "Use the budget tool to manage income and expenses\n. You can adjust tax rates and allocate funds",
                                 "Experiment with different policies to boost your\n city's economy and happiness",
                                 "Deal with natural disasters such as earthquakes,\n fires, and tornadoes that may occur in your city",
                                 "Finally, aim to achieve specific goals \nsuch as reaching a certain population"]

        # Set up positions
        self.menu_title_pos = (self.screen_width // 2, 100)
        self.menu_option_start_pos = (self.screen_width // 2, 250)
        self.menu_option_spacing = 75
        self.options_title_pos = (self.screen_width // 2, 100)
        self.options_option_start_pos = (self.screen_width // 2, 250)
        self.options_option_spacing = 75

        # Set up map
        self.map_image = pygame.image.load("./Map/Assets/simCity.jpg")
        self.map_rect = self.map_image.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2))

        # Set up game loop
        self.running = True
        self.menu_mode = True
        self.start_menu = True
        self.start_game = False
        self.current_option = 0
        self.show_instructions = False
        self.loaded_game = False
        self.flag = True

    def draw_instructions(self):
        # Draw a semi-transparent black rectangle to create a background
        background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 128))
        self.screen.blit(background, (0, 0))

        # Draw the instruction text on the screen
        for i, text in enumerate(self.instruction_text):
            text_surface = self.instruction_font.render(text, True, self.white)
            text_rect = text_surface.get_rect(center=(
                self.screen_width // 2, self.screen_height // 2 + i * 50 - ((len(self.instruction_text)-1)*25)))
            self.screen.blit(text_surface, text_rect)

        self.show_instructions = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_buttondown_event(event)

    def handle_keydown_event(self, event):
        if self.menu_mode:
            self.handle_keydown_event_menu(event)
        else:
            self.handle_keydown_event_options(event)

    def handle_keydown_event_menu(self, event):
        if event.key == pygame.K_UP:
            self.current_option = (self.current_option -
                                   1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.current_option = (self.current_option +
                                   1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN:
            if self.current_option == 0:
                print("New Game selected")
                self.start_menu = False
                self.start_game = True
            elif self.current_option == 1:
                self.menu_mode = False
                self.current_option = 0
            elif self.current_option == 2:
                print("Load Game selected")
                self.loaded_game = True
                self.start_menu = False
                self.start_game = True
            elif self.current_option == 3:
                self.running = False
        elif event.key == pygame.K_ESCAPE:
            self.menu_mode = True
            self.current_option = 0

    def handle_keydown_event_options(self, event):
        if event.key == pygame.K_RETURN:
            if self.current_option == 0:
                print("Resume selected")
                # TODO: RESUME THE ALREADY STARTED GAME
            elif self.current_option == 1:
                print("Instructions selected")
                self.show_instructions = True
            elif self.current_option == 2:
                print("Save selected")
                # TODO: SAVE THE STATUS OF THE CURRENT GAME
            elif self.current_option == 3:
                self.menu_mode = True
                self.current_option = 0

    def handle_mouse_buttondown_event(self, event):
        if self.menu_mode:
            self.handle_mouse_buttondown_event_menu(event)
        else:
            self.handle_mouse_buttondown_event_options(event)

    def handle_mouse_buttondown_event_menu(self, event):
        for i, option in enumerate(self.menu_options):
            option_text = self.menu_font.render(option[0], True, self.white)
            option_rect = option_text.get_rect(center=(
                self.menu_option_start_pos[0],
                self.menu_option_start_pos[1] + i * self.menu_option_spacing,
            ))
            if option_rect.collidepoint(event.pos):
                self.current_option = i
                if i == 0:
                    print("New Game selected")
                elif i == 1:
                    self.menu_mode = False
                    self.current_option = 0
                elif i == 2:
                    print("Load Game selected")
                elif i == 3:
                    self.running = False

    def handle_mouse_buttondown_event_options(self, event):
        for i, option in enumerate(self.options_options):
            option_text = self.menu_font.render(option[0], True, self.white)
            option_rect = option_text.get_rect(center=(
                self.options_option_start_pos[0],
                self.options_option_start_pos[1] +
                i * self.options_option_spacing,
            ))
            if option_rect.collidepoint(event.pos):
                self.current_option = i
                if i == 0:
                    print("Resume selected")
                    self.resume_game()
                elif i == 1:
                    print("Instructions selected")
                    self.show_instructions()
                elif i == 2:
                    print("Save selected")
                    self.save_game()
                elif i == 3:
                    self.menu_mode = True
                    self.current_option = 0

    def draw_screen(self):
        self.screen.fill(self.black)
        self.screen.blit(self.map_image, self.map_rect)
        if self.menu_mode:
            self.draw_menu()
        else:
            self.draw_options()
        pygame.display.update()

    def draw_menu(self):
        menu_title_text = self.selected_font.render(
            "Main Menu", True, self.selected_color)
        menu_title_rect = menu_title_text.get_rect(center=self.menu_title_pos)
        self.screen.blit(menu_title_text, menu_title_rect)
        for i, option in enumerate(self.menu_options):
            option_text = self.menu_font.render(option[0], True, self.white)
            option_rect = option_text.get_rect(center=(
                self.menu_option_start_pos[0],
                self.menu_option_start_pos[1] + i * self.menu_option_spacing,
            ))
            if i == self.current_option:
                selected_text = self.selected_font.render(
                    option[0], True, self.selected_color)
                selected_rect = selected_text.get_rect(center=(
                    self.menu_option_start_pos[0],
                    self.menu_option_start_pos[1] +
                    i * self.menu_option_spacing,
                ))
                self.screen.blit(selected_text, selected_rect)
            else:
                self.screen.blit(option_text, option_rect)

    def draw_options(self):
        if self.current_option == 1:
            if self.show_instructions:
                self.draw_instructions()
        else:
            options_title_text = self.selected_font.render(
                "Options", True, self.selected_color)
            options_title_rect = options_title_text.get_rect(
                center=self.options_title_pos)
            self.screen.blit(options_title_text, options_title_rect)
            for i, option in enumerate(self.options_options):
                option_text = self.menu_font.render(
                    option[0], True, self.white)
                option_rect = option_text.get_rect(center=(
                    self.options_option_start_pos[0],
                    self.options_option_start_pos[1] +
                    i * self.options_option_spacing,
                ))
                if i == self.current_option:
                    selected_text = self.selected_font.render(
                        option[0], True, self.selected_color)
                    selected_rect = selected_text.get_rect(center=(
                        self.options_option_start_pos[0],
                        self.options_option_start_pos[1] +
                        i * self.options_option_spacing,
                    ))
                    self.screen.blit(selected_text, selected_rect)
                else:
                    self.screen.blit(option_text, option_rect)

    def resume_game(self):
        print("Resume selected")
        # TODO: RESUME THE ALREADY STARTED GAME

    def save_game(self):
        print("Save selected")
        # TODO: SAVE THE STATUS OF THE CURRENT GAME

    def start_new_game(self):
        print("New Game selected")
        self.start_menu = False
        self.start_game = True

    def load_game(self):
        print("Load Game selected")
        self.loaded_game = True
        self.start_menu = False
        self.start_game = True

    def show_instructions(self):
        print("Instructions selected")
        self.show_instructions = True

    def exit_game(self):
        self.running = False

    def display_menu(self):
        while self.running:
            self.handle_events()
            self.draw_screen()
            if self.start_game:
                self.start_menu = True
                self.start_game = False
                allocated_tax = 0.5  # should be loaded!!
                if not self.loaded_game:
                    taskAllocator = TaskAllocator()
                    taskAllocator.run()
                    allocated_tax = float(taskAllocator.get_input_text())
                main.run(self.running, self.loaded_game,
                         self.flag, allocated_tax)
