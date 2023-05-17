import datetime, pygame

class Timer:
    """A class for keeping track of time in a game.
    
    Attributes:
        time (pygame.time.Clock): A clock object from the Pygame library used to track the passage of time.
        time_factor (float): The conversion factor between game time (in seconds) and real-world time (also in seconds).
    
    Methods:
        get_current_time(): Returns the current date and time as a datetime object.
        get_current_date_str(): Returns the current date as a string in the format 'YYYY-MM-DD'.
        tick(n: int): Advances the timer by n game frames.
    """


    def __init__(self, game_speed: int, game_speed_multiplier: int):
        """Constructor for the Timer class.

        Args:
         game_speed (int): The desired speed of the game in frames per second.
            game_speed_multiplier (int): The multiplier to apply to the time factor to make the game time pass faster.
     """
        self.clock = pygame.time.Clock()
        self.game_speed_multiplier = game_speed_multiplier
        self.game_speed = game_speed
        self.time_factor = (60 / self.game_speed) * self.game_speed_multiplier
        self.current_time = datetime.datetime.now()

    def get_time_factor(self):
        return (60 / self.game_speed) * self.game_speed_multiplier

    def get_current_time(self) -> datetime.datetime:
        """Returns the current date and time as a datetime object."""
        return self.current_time

    def get_current_date_str(self) -> str:
        """Returns the current date as a string in the format 'YYYY-MM-DD'."""
        return self.get_current_time().strftime('%Y-%m-%d')
    
    def tick(self, n: int):
        """Advances the timer by n game frames.
        
        Args:
            n (int): The number of game frames to advance the timer by.
        """
        self.clock.tick(n)
    
    def update_time(self, paused: bool) -> None:
        """
        Update the current time of the timer based on the game's time factor and pause state.
        
        Args:
            paused (bool): Indicates whether the game is currently paused or not.
        
        Returns:
            None
        """
        if not paused:
            self.current_time += datetime.timedelta(seconds=self.get_time_factor())
        
    def subtract_with_time_str(self,date_str: str) -> int:
        """With a given formatted string 'YYYY-MM-DD', returns the difference in days between the current
        time object and the given string"""
        x = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        delta = self.get_current_time() - x
        diff_in_days = delta.days
        return diff_in_days
    
    def get_timer_from_str(self,str_date):
        return datetime.datetime.strptime(str_date, "%Y-%m-%d")