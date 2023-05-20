import random


class Tile:
    """A class representing a tile in a game map.

    Attributes:
        x (int): The x-coordinate of the tile.
        y (int): The y-coordinate of the tile.
        type (str): The type of the tile.
        occupied (bool): Flag indicating if the tile is occupied.

    Methods:
        None
    """

    def __init__(self, x, y, type, occupied):
        """Initialize the Tile object.

        Args:
            x (int): The x-coordinate of the tile.
            y (int): The y-coordinate of the tile.
            type (str): The type of the tile.
            occupied (bool): Flag indicating if the tile is occupied.
        """
        self.x = x
        self.y = y
        self.type = type
        self.occupied = occupied