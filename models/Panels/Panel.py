import pygame


class Panel:
    """
    A class representing a panel in a graphical user interface.
    
    Attributes:
        x (int): The x-coordinate of the panel's position.
        y (int): The y-coordinate of the panel's position.
        width (int): The width of the panel.
        height (int): The height of the panel.
    """

    def __init__(self, x, y, width, height):
        """
        Initializes a Panel object.
        
        Args:
            x (int): The x-coordinate of the panel's position.
            y (int): The y-coordinate of the panel's position.
            width (int): The width of the panel.
            height (int): The height of the panel.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def display(self, screen, font_size, text_position, color, text, text_color):
        """
        Display the panel on the screen.
        
        Args:
            screen (pygame.Surface): The surface to blit the panel on.
            font_size (int): The font size of the text.
            text_position (tuple): The position of the text (x, y).
            color (tuple): The color of the panel (R, G, B).
            text (str): The text to display on the panel.
            text_color (tuple): The color of the text (R, G, B).
        """
        pygame.draw.rect(
            screen, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_position)

    def get_width(self):
        """
        Get the width of the panel.
        Returns:
            int: The width of the panel.
        """
        return self.width

    def get_height(self):
        """
        Get the height of the panel.
        
        Returns:
            int: The height of the panel.
        """
        return self.height
