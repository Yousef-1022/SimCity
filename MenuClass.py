import pygame
import main
import pickle
from models.TaxAllocator import TaskAllocator


class MenuClass:
    """
    Represents the game menu.

    Attributes:
    - screen_width (int): The width of the game screen.
    - screen_height (int): The height of the game screen.
    - screen (pygame.Surface): The game screen surface.
    - instruction_font (pygame.font.Font): The font used for instruction text.
    - menu_font (pygame.font.Font): The font used for menu options.
    - selected_font (pygame.font.Font): The font used for the selected menu option.
    - black (tuple): The RGB color value for black.
    - white (tuple): The RGB color value for white.
    - selected_color (tuple): The RGB color value for the selected menu option.
    - menu_options (list): A list of tuples representing the menu options and their selection status.
    - options_options (list): A list of tuples representing the options menu options and their selection status.
    - instruction_text (list): A list of strings representing the instruction text.
    - menu_title_pos (tuple): The position of the menu title.
    - menu_option_start_pos (tuple): The starting position of the menu options.
    - menu_option_spacing (int): The spacing between menu options.
    - options_title_pos (tuple): The position of the options title.
    - options_option_start_pos (tuple): The starting position of the options menu options.
    - options_option_spacing (int): The spacing between options menu options.
    - map_image (pygame.Surface): The image representing the game map.
    - map_rect (pygame.Rect): The rectangle representing the map image.
    - running (bool): Flag indicating if the game is running.
    - menu_mode (bool): Flag indicating if the game is in menu mode.
    - start_menu (bool): Flag indicating if the game should start from the menu.
    - start_game (bool): Flag indicating if the game should start a new game.
    - current_option (int): The index of the currently selected menu option.
    - show_instructions (bool): Flag indicating if the instructions should be shown.
    - loaded_game (bool): Flag indicating if a saved game is loaded.
    - flag (bool): A flag used for internal game logic.

    Methods:
    - draw_instructions(): Draws the instruction text on the screen.
    - handle_events(): Handles the game events such as key presses and mouse clicks.
    - handle_keydown_event(event): Handles the keydown event.
    - handle_keydown_event_menu(event): Handles the keydown event in the menu mode.
    - handle_keydown_event_options(event): Handles the keydown event in the options mode.
    - handle_mouse_buttondown_event(event): Handles the mouse buttondown event.
    - handle_mouse_buttondown_event_menu(event): Handles the mouse buttondown event in the menu mode.
    - handle_mouse_buttondown_event_options(event): Handles the mouse buttondown event in the options mode.
    - draw_screen(): Draws the game screen.
    - draw_menu(): Draws the menu on the screen.
    - draw_options(): Draws the options menu on the screen.
    - start_new_game(): Starts a new game.
    - load_game(): Loads a saved game.
    - draw_instructions(): Displays the game instructions.
    - exit_game(): Exits the game.
    - display_menu(): Displays the game menu and handles user input.
    """
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
            ("Instructions", False),
            ("Main Menu", False),
        ]

        self.instruction_text = [
            "Introduction:",
            "Begin the game with 10 initial citizens and embark on your mission to develop thriving Residential Zones and Work Zones.",
            "Manage a starting budget of $100,000, ensuring it remains positive to uphold citizen satisfaction.",
            "Zone Information:",
            "Work Zones encompass Industrial Zones and Service Zones, which can be upgraded to accommodate a growing population.",
            "Establish efficient road connections between Residential Zones and desired Work Zones to facilitate citizen movement.",
            "Annual income is generated based on the Tax Rate and the population of each Work Zone, contributing to the city's financial stability.",
            "Satisfaction Information:",
            "Uphold high levels of citizen satisfaction to retain a content population and prevent citizens from leaving the city.",
            "Enhance citizen satisfaction by strategically constructing Stadiums, Police Departments, and Forests throughout the city.",
            "Optimize the placement of satisfaction-boosting structures by locating them in proximity to Residential Zones for maximum impact.",
            "Forge strong Residential Zone to Work Zone connections through a well-designed network of Roads, enabling smooth citizen transitions.",
            "Otherwise, if a Residential Zone is not connected to a Work Zone then the Work Zone was created in vain.",
            "When a Citizen needs to travel to a distant Work Zone, their satisfaction level is adversely affected.",
            "Demolish, and Disaster Information:",
            "Be vigilant of the rare occurrence of natural fire disasters, with the likelihood increasing as more forests are developed annually.",
            "A disaster removes Citizens from the game only if it happens on an RZone. Other structures are destroyed!",
            "Demolishing a WorkZone results in all its Citizens becoming unemployed, and it becomes crucial to provide them with an alternative route.",
            "In the event of demolishing a ResidentialZone without providing an alternative option, the Citizens residing there will become homeless,",
            "potentially leading to their departure from the city. Ensure good connections among the Zones to avoid such issues!",
            "Navigation:",
            "Use the Arrow keys to navigate in the map, you are able to go: North, South, West, East.",
            "Use the Right Mouse Button on a structure to show its relevant information. Only forests cannot be clicked.",
            "Use the Bulldozer icon (1st Icon) to destory a certain Road. Be ware! A Road connecting between an RZone and WZone can't be destroyed!"
        ]

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
        self.new_game_flag = False

    def draw_instructions(self):
        """
        Draws the instruction text on the screen.

        This method fills a semi-transparent black rectangle as the background and
        renders the instruction text on the screen.

        Args:
            None

        Returns:
            None
        """
        # Draw a semi-transparent black rectangle to create a background
        background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 191))
        self.screen.blit(background, (0, 0))

        # Draw the instruction text on the screen
        vertical_offset = - (self.screen_width // 3)
        line_spacing = 30
        for i, text in enumerate(self.instruction_text):
            text_surface = self.instruction_font.render(text, True, self.white)
            text_rect = text_surface.get_rect(center=(
                self.screen_width // 2, self.screen_height // 2 + i * line_spacing + vertical_offset))
            self.screen.blit(text_surface, text_rect)


    def handle_events(self):
        """
        Handles events such as key presses and mouse button clicks.

        This method iterates through the events in the Pygame event queue and
        handles different types of events. It can handle events such as quitting
        the game, key presses, and mouse button clicks.

        Args:
            None

        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_buttondown_event(event)

    def handle_keydown_event(self, event):
        """
        Handles keydown events.

        This method is responsible for handling keydown events. It determines
        whether the game is currently in menu mode or options mode and calls the
        respective handler method based on the current mode.

        Args:
            event (pygame.event.Event): The Pygame event object representing the
                keydown event.

        Returns:
            None
        """
        if self.menu_mode:
            self.handle_keydown_event_menu(event)
        else:
            self.handle_keydown_event_options(event)

    def handle_keydown_event_menu(self, event):
        """
        Handles keyboard events in MainMenu mode.
        
        This method is called when a keydown event occurs in MainMenu mode.
        It checks the key that was pressed and performs the corresponding action
        based on the current selected option.
        
        Args:
            event (pygame.event.Event): The Pygame event object representing the
                keydown event.

        Returns:
            None
        """
        if event.key == pygame.K_UP:
            self.current_option = (self.current_option -
                                   1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.current_option = (self.current_option +
                                   1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN:
            if self.current_option == 0:
                self.initialize_start_new_game_vars()
            elif self.current_option == 1:
                self.menu_mode = False
                self.current_option = 0
            elif self.current_option == 2:
                self.initialize_start_load_game_vars()
            elif self.current_option == 3:
                self.running = False
        elif event.key == pygame.K_ESCAPE:
            self.menu_mode = True
            self.current_option = 0

    def handle_keydown_event_options(self, event):
        """
        Handles keydown events in options mode.

        This method is called when a keydown event occurs in options mode.
        It checks the key that was pressed and performs the corresponding action
        based on the current selected option.

        Args:
            event (pygame.event.Event): The Pygame event object representing the
                keydown event.

        Returns:
            None
        """
        self.show_instructions = False
        if event.key == pygame.K_UP:
            self.current_option = (self.current_option -
                                   1) % len(self.options_options)
        elif event.key == pygame.K_DOWN:
            self.current_option = (self.current_option +
                                   1) % len(self.options_options)
        elif event.key == pygame.K_RETURN:
            if self.current_option == 0:
                self.show_instructions = True
            else:
                self.menu_mode = True
                self.current_option = 0
        elif event.key == pygame.K_ESCAPE:
            self.menu_mode = True
            self.current_option = 0

    def handle_mouse_buttondown_event(self, event):
        """
        Handles mouse buttondown events.

        This method is called when a mouse buttondown event occurs.
        It checks the current mode (menu or options) and calls the corresponding
        method to handle the event.

        Args:
            event (pygame.event.Event): The Pygame event object representing the
                mouse buttondown event.

        Returns:
            None
        """
        if self.menu_mode:
            self.handle_mouse_buttondown_event_menu(event)
        else:
            self.handle_mouse_buttondown_event_options(event)

    def handle_mouse_buttondown_event_menu(self, event):
        """
        Handles mouse buttondown events in the menu mode.

        This method is called when a mouse buttondown event occurs in the menu mode.
        It checks if any menu option is clicked based on the position of the mouse click,
        updates the current option accordingly, and performs the corresponding action.

        Args:
            event (pygame.event.Event): The Pygame event object representing the
                mouse buttondown event.

        Returns:
            None
        """
        for i, option in enumerate(self.menu_options):
            option_text = self.menu_font.render(option[0], True, self.white)
            option_rect = option_text.get_rect(center=(
                self.menu_option_start_pos[0],
                self.menu_option_start_pos[1] + i * self.menu_option_spacing,
            ))
            if option_rect.collidepoint(event.pos):
                self.current_option = i
                if i == 0:
                    self.initialize_start_new_game_vars()
                elif i == 1:
                    self.menu_mode = False
                    self.current_option = 0
                elif i == 2:
                    self.initialize_start_load_game_vars()
                elif i == 3:
                    self.running = False

    def handle_mouse_buttondown_event_options(self, event):
        """
        Handles mouse buttondown events in the options mode.

        This method is called when a mouse buttondown event occurs in the options mode.
        It checks if any options option is clicked based on the position of the mouse click,
        updates the current option accordingly, and performs the corresponding action.

        Args:
            event (pygame.event.Event): The Pygame event object representing the
                mouse buttondown event.

        Returns:
            None
        """
        self.show_instructions = False
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
                    self.show_instructions = True
                else:
                    self.menu_mode = True
                    self.current_option = 0

    def draw_screen(self):
        """
        Draws the screen.

        This method is responsible for drawing the screen based on the current mode.
        It fills the screen with the color black, blits the map image onto the screen,
        and then calls either the `draw_menu` or `draw_options` method based on the
        current mode. Finally, it updates the Pygame display.

        Args:
            None

        Returns:
            None
        """
        self.screen.fill(self.black)
        self.screen.blit(self.map_image, self.map_rect)
        if self.menu_mode:
            self.draw_menu()
        else:
            self.draw_options()
        pygame.display.update()

    def draw_menu(self):
        """
        Draws the menu.

        This method is responsible for drawing the menu on the screen.
        It renders the menu title text and blits it onto the screen.
        It then iterates over the menu options, renders each option text,
        and blits it onto the screen. If an option is the currently selected
        option, it renders the text using a different font and color to indicate
        the selection. Finally, it updates the Pygame display.

        Args:
            None

        Returns:
            None
        """
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
        """
        Draws the options.

        This method is responsible for drawing the options on the screen.
        If the current option is 1 and the instructions are set to be shown,
        it calls the `draw_instructions` method to draw the instructions.
        Otherwise, it renders the options title text and blits it onto the screen.
        It then iterates over the options options, renders each option text,
        and blits it onto the screen. If an option is the currently selected
        option, it renders the text using a different font and color to indicate
        the selection. Finally, it updates the Pygame display.

        Args:
            None

        Returns:
            None
        """
            
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
                
        if self.show_instructions:
            self.draw_instructions()


    def initialize_start_new_game_vars(self):
        """
        Changes the variables of the MenuClass when `New Game` is clicked to as follows:
        
        `new_game_flag` = `True`
        
        `loaded_game` to `False`
        
        `start_menu` = `False`
        
        `start_game` = `True`
        """
        
        self.new_game_flag = True
        self.loaded_game = False
        self.start_menu = False
        self.start_game = True

    def initialize_start_load_game_vars(self):
        """
        Changes the variables of the MenuClass when `Load Game` is clicked to as follows:
        
        `new_game_flag` = `False`
        
        `loaded_game` to `True`
        
        `start_menu` = `False`
        
        `start_game` = `True`
        """
        
        self.new_game_flag = False
        self.loaded_game = True
        self.start_menu = False
        self.start_game = True


    def exit_game(self):
        self.running = False

    def display_menu(self):
        """
        Displays the menu.

        This method is responsible for displaying the menu on the screen.
        It contains a while loop that runs as long as the `running` flag is True.
        Within the loop, it calls the `handle_events` method to handle user events,
        the `draw_screen` method to draw the screen, and checks if `start_game`
        is True. If `start_game` is True, it sets `start_menu` to True, `start_game`
        to False, and initializes the `allocated_tax` variable to 0.5.

        If `loaded_game` is False, it creates a new instance of `TaskAllocator`,
        runs it, and retrieves the allocated tax value from the instance.
        Otherwise, it uses the loaded allocated tax value.

        Finally, it calls the `run` method of the `main` module passing the
        `running`, `loaded_game`, `flag`, and `allocated_tax` values.

        Args:
            None

        Returns:
            None
        """
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
                         self.new_game_flag, allocated_tax)
