import pygame
from models.Panels.Panel import Panel

class BuilderPanel(Panel):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.icons = []  # list to store the loaded icon images
        self.icon_size = 70  # size of each icon image
        self.icon_spacing = 10  # spacing between each icon
        self.num_icons_per_row = 1  # number of icons to display per row

    def load_icons(self, icon_filenames):
        """Load the icon images and store them in self.icons."""
        for filename in icon_filenames:
            icon_image = pygame.image.load(filename)
            self.icons.append(icon_image)

    def display_assets(self, screen, icon_filenames):
        """Display the loaded icon images on the BuilderPanel."""
        self.icons = [] 
        self.load_icons(icon_filenames)
        # Calculate the size and position of the table cells
        cell_width = self.icon_size + self.icon_spacing
        cell_height = self.icon_size + self.icon_spacing
        num_rows = len(self.icons)
        table_width = cell_width
        table_height = cell_height * num_rows + self.icon_spacing
        table_x = (self.width - table_width) // 2
        table_y = self.y

        # Draw the table border
        pygame.draw.rect(screen, (255, 255, 255), (table_x, table_y, table_width, table_height), 2)

        # Draw the icon images with borders
        for i, icon_image in enumerate(self.icons):
            icon_x = table_x + self.icon_spacing
            icon_y = table_y + i * cell_height + self.icon_spacing
            
            # Draw the icon border
            border_rect = pygame.Rect(icon_x - 2, icon_y - 2, self.icon_size + 4, self.icon_size + 4)
            pygame.draw.rect(screen, (255, 255, 255), border_rect, 2)
            
            screen.blit(icon_image, (icon_x, icon_y))

    def get_selected_icon_index(self, mouse_pos):
        for i, icon_image in enumerate(self.icons):
            icon_x = self.x + self.icon_spacing
            icon_y = self.y + i * (self.icon_size + self.icon_spacing) + self.icon_spacing
            icon_rect = pygame.Rect(icon_x, icon_y, self.icon_size, self.icon_size)
            if icon_rect.collidepoint(mouse_pos):
                return i
        return None
