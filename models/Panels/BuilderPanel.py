import pygame
from models.Panels.Panel import Panel


class BuilderPanel(Panel):
    """
    A class representing a builder panel in a graphical user interface.
    
    Attributes:
        x (int): The x-coordinate of the panel's position.
        y (int): The y-coordinate of the panel's position.
        width (int): The width of the panel.
        height (int): The height of the panel.
        icons (list): A list to store the loaded icon images.
        icon_size (int): The size of each icon image.
        icon_spacing (int): The spacing between each icon.
        num_icons_per_row (int): The number of icons to display per row.
    """

    def __init__(self, x, y, width, height):
        """
        Initializes a BuilderPanel object.
        
        Args:
            x (int): The x-coordinate of the panel's position.
            y (int): The y-coordinate of the panel's position.
            width (int): The width of the panel.
            height (int): The height of the panel.
        """
        super().__init__(x, y, width, height)
        self.icons = []
        self.icon_size = 70
        self.icon_spacing = 10
        self.num_icons_per_row = 1

    def load_icons(self, icon_filenames):
        """
        Load the icon images and store them in self.icons.
        
        Args:
            icon_filenames (list): A list of filenames of the icon images to load.
        """
        for filename in icon_filenames:
            icon_image = pygame.image.load(filename)
            self.icons.append(icon_image)

    def display_assets(self, screen, icon_filenames):
        """
        Display the loaded icon images on the BuilderPanel.
        
        Args:
            screen (pygame.Surface): The surface to blit the images on.
            icon_filenames (tuple): A tuple of filenames of the icon images to display.
        """
        self.icons = []
        self.load_icons([f[0] for f in icon_filenames])

        # Calculate the size and position of the table cells
        cell_width = self.icon_size + self.icon_spacing
        cell_height = self.icon_size + self.icon_spacing
        num_rows = len(self.icons)
        table_width = cell_width
        table_height = cell_height * num_rows + self.icon_spacing
        table_x = (self.width - table_width) // 2
        table_y = self.y

        # Draw the table border
        pygame.draw.rect(screen, (255, 255, 255),
                         (table_x, table_y, table_width, table_height), 2)

        # Draw the icon images with borders
        for i, icon_image in enumerate(self.icons):
            icon_x = table_x + self.icon_spacing
            icon_y = table_y + i * cell_height + self.icon_spacing

            # Draw the icon border
            border_rect = pygame.Rect(
                icon_x - 2, icon_y - 2, self.icon_size + 4, self.icon_size + 4)
            pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)

            screen.blit(icon_image, (icon_x, icon_y))

    def get_selected_icon_index(self, mouse_pos):
        """
        Get the index of the selected icon based on the mouse position.
        
        Args:
            mouse_pos (tuple): The position of the mouse (x, y).
            
        Returns:
            int or None: The index of the selected icon, or None if no icon is selected.
        """
        for i, icon_image in enumerate(self.icons):
            icon_x = self.x + self.icon_spacing
            icon_y = self.y + i * \
                (self.icon_size + self.icon_spacing) + self.icon_spacing
            icon_rect = pygame.Rect(
                icon_x, icon_y, self.icon_size, self.icon_size)
            if icon_rect.collidepoint(mouse_pos):
                return i
        return None
