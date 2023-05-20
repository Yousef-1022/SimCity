import pygame
import sys


class TaskAllocator:
    """A class representing a user interface for allocating tax in a city simulation game.

    Attributes:
        screen_width (int): The width of the pygame screen.
        screen_height (int): The height of the pygame screen.
        screen (pygame.Surface): The pygame screen object.
        container_rect (pygame.Rect): The rectangular area for the main container.
        input_rect (pygame.Rect): The rectangular area for the input field.
        button_rect (pygame.Rect): The rectangular area for the button.
        clock (pygame.time.Clock): The pygame clock object.
        map_image (pygame.Surface): The background map image.
        font (pygame.font.Font): The font used for text rendering.
        button_font (pygame.font.Font): The font used for button text rendering.
        input_text (str): The current text entered in the input field.
        is_input_active (bool): Flag indicating if the input field is active for text input.
        button_text (str): The text displayed on the button.
        should_exit (bool): Flag indicating if the program should exit.

    Methods:
        handle_events(): Handle pygame events.
        draw(): Draw the user interface elements on the screen.
        run(): Run the main loop of the program.
        get_input_text(): Get the current text entered in the input field.
    """

    def __init__(self):
        """Initialize the TaskAllocator object."""
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        # Calculate positions based on the screen dimensions
        container_width = 400
        container_height = 200
        self.container_rect = pygame.Rect(self.screen_width // 2 - container_width // 2,
                                          self.screen_height // 2 - container_height // 2,
                                          container_width, container_height)
        self.input_rect = pygame.Rect(self.container_rect.left + 100,
                                      self.container_rect.top + 100,
                                      200, 30)
        self.button_rect = pygame.Rect(self.container_rect.left + 150,
                                       self.container_rect.top + 150,
                                       100, 30)
        self.clock = pygame.time.Clock()
        self.map_image = pygame.image.load("./Map/Assets/simCity.jpg")

        self.font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 24)
        self.input_text = ''
        self.is_input_active = False
        self.button_text = 'Allocate tax'
        self.should_exit = False  # Flag to indicate if the current instance should exit

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.is_input_active = True
                else:
                    self.is_input_active = False
                if self.button_rect.collidepoint(event.pos):
                    try:
                        input_value = float(self.input_text)
                        if 0 <= input_value <= 1:
                            self.should_exit = True
                    except ValueError:
                        # Invalid input value (not a valid float)
                        pass
            elif event.type == pygame.KEYDOWN:
                if self.is_input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            input_value = float(self.input_text)
                            if 0 <= input_value <= 1:
                                self.should_exit = True
                        except ValueError:
                            # Invalid input value (not a valid float)
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

    def draw(self):
        """Draw the user interface elements on the screen."""
        # Blit the background image at (0, 0)
        self.screen.blit(self.map_image, (0, 0))

        # Create a semi-transparent overlay for the container
        overlay_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        # Adjust the transparency value (fourth element) as desired
        overlay_surface.fill((0, 0, 0, 100))
        self.screen.blit(overlay_surface, (0, 0))

        # Semi-transparent container background
        pygame.draw.rect(self.screen, (70, 130, 180, 200),
                         self.container_rect, border_radius=5)

        # Render the title text
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render(
            "Tax Allocation", True, (255, 255, 255))  # Title text color
        title_text_rect = title_text.get_rect(
            centerx=self.container_rect.centerx, top=self.container_rect.top + 40)  # Adjust vertical position
        self.screen.blit(title_text, title_text_rect)

        pygame.draw.line(self.screen, (255, 255, 255), (self.container_rect.left + 30, title_text_rect.bottom + 10),
                         (self.container_rect.right - 30, title_text_rect.bottom + 10), 2)  # Line breaker

        # Input field color (white)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         self.input_rect, border_radius=5)
        text_surface = self.font.render(
            self.input_text, True, (70, 130, 180))  # Input text color (blue)
        text_rect = text_surface.get_rect(center=self.input_rect.center)
        self.screen.blit(text_surface, text_rect)

        # Button background color
        pygame.draw.rect(self.screen, (70, 130, 180),
                         self.button_rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect,
                         width=2, border_radius=5)  # Button border
        button_text_surface = self.button_font.render(
            self.button_text, True, (255, 255, 255))  # Button text color
        button_text_rect = button_text_surface.get_rect(
            center=self.button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        """Run the main loop of the program."""
        while not self.should_exit:
            self.handle_events()
            self.draw()

    def get_input_text(self):
        """Get the current text entered in the input field.

        Returns:
            str: The text entered in the input field.
        """
        return self.input_text
