import random

class Citizen:
    """
    A class representing a citizen in a city simulation game.
    
    Attributes:
        citizens (dict): A dictionary containing all the citizens.
        next_id (int): The ID to assign to the next created citizen.
        home (Zone): The home zone of the citizen.
        work (Zone): The work zone of the citizen.
        satisfaction (int): The satisfaction level of the citizen.
        id (int): The ID of the citizen.
    """
    citizens = {}
    next_id = 1
    
    def __init__(self):
        """
        Initializes a Citizen object.
        """
        self.home = None
        self.work = None
        self.satisfaction = random.randint(50, 100)
        self.id = Citizen.next_id
        Citizen.next_id += 1
        Citizen.citizens[self.id] = self

    @classmethod
    def get_citizens_len(cls):
        """
        Returns the number of citizens.
        
        Returns:
            int: The number of citizens.
        """
        return len(Citizen.citizens)

    @classmethod
    def get_all_citizens(cls):
        """
        Returns a copy of the citizens dictionary.
        
        Returns:
            dict: A copy of the citizens dictionary.
        """
        return cls.citizens.copy()

    @classmethod
    def get_home(cls):
        """
        Returns the ID of the citizen's home zone.
        
        Returns:
            int or str: The ID of the citizen's home zone, or an empty string if the citizen has no home.
        """
        if cls.home:
            return cls.home.id
        return ""

    @classmethod
    def get_work(cls):
        """
        Returns the ID of the citizen's work zone.
        
        Returns:
            int or str: The ID of the citizen's work zone, or an empty string if the citizen has no work.
        """
        if cls.work:
            return cls.work.id
        return ""

    @classmethod
    def get_satisfaction(cls):
        """
        Returns the satisfaction level of the citizen.
        
        Returns:
            int: The satisfaction level of the citizen.
        """
        return cls.satisfaction
