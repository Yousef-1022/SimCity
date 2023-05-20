class Player:
    """
    A class representing a player in a city simulation game.

    Attributes:
        name (str): The name of the player.
        money (float): The amount of money the player has.
    """

    def __init__(self, name, money):
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player.
            money (float): The initial amount of money for the player.
        """
        self.name = name
        self.money = money
