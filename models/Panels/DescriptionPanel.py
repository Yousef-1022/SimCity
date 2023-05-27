import pygame
from models.Panels.Panel import Panel


class DescriptionPanel(Panel):
    def __init__(self, x, y, width, height):
        """
        Initializes a DescriptionPanel object.
        
        Args:
            x (int): The x-coordinate of the panel's position.
            y (int): The y-coordinate of the panel's position.
            width (int): The width of the panel.
            height (int): The height of the panel.
        """
        self.slider_position = 0  # The current position of the slider (0, 1, or 2)
        super().__init__(x, y, width, height)

    def display_time(self, screen, time, text_position):
        """
        Display the time on the DescriptionPanel.
        
        Args:
            screen (pygame.Surface): The surface to blit the text on.
            time (str): The time to display.
            text_position (tuple): The position of the text (x, y).
        """
        font = pygame.font.Font(None, 21)
        text_surface = font.render(time, True, (0, 0, 0))
        screen.blit(text_surface, text_position)

    def handle_game_speed_click(self, event, timer, game_speed_multiplier):
        """
        Handle the click event for the game speed buttons.
        
        Args:
            event (pygame.event.Event): The pygame event object.
            timer (Timer): The timer object.
            game_speed_multiplier (list): A list of game speed multipliers.
        """
        button_width = 80
        button_height = 30
        button_spacing = 20

        label_x = self.x + (self.width - (button_width *
                            3 + button_spacing * 2)) - 120
        label_y = self.y + self.height - button_height - 5

        mouse_x, mouse_y = event.pos
        button_x = label_x + button_width + button_spacing
        button_y = label_y + 5  # Calculate button_y based on label_y
        for i in range(3):
            button_rect = pygame.Rect(
                button_x, button_y, button_width, button_height)
            if button_rect.collidepoint(mouse_x, mouse_y):
                chosen_speed = i
                timer.game_speed_multiplier = game_speed_multiplier[i]
                break
            button_x += button_width + button_spacing

    def display_game_speed(self, screen, timer, game_speed_multiplier):
        """
        Display the game speed buttons on the DescriptionPanel.
        
        Args:
            screen (pygame.Surface): The surface to blit the buttons on.
            timer (Timer): The timer object.
            game_speed_multiplier (list): A list of game speed multipliers.
        """
        button_width = 80
        button_height = 30
        button_spacing = 20

        label_x = self.x + (self.width - (button_width *
                            3 + button_spacing * 2)) - 120
        label_y = self.y + self.height - button_height - 5

        pygame.draw.rect(screen, (128, 128, 128), (label_x, label_y,
                         button_width * 3 + button_spacing * 2, button_height))

        font = pygame.font.Font(None, 21)
        label_text = font.render("Game Speed:", True, (0, 0, 0))
        screen.blit(label_text, (label_x + 10, label_y + 14))

        # Red, Yellow, Green for buttons
        button_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
        button_labels = ["Slow", "Medium", "Fast"]
        button_x = label_x + button_width + button_spacing
        button_y = label_y + 5

        for i in range(3):
            button_rect = pygame.Rect(
                button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, button_colors[i], button_rect)
            button_text = font.render(button_labels[i], True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)
            button_x += button_width + button_spacing
