from models.Panels.Panel import Panel
class PricePanel(Panel):
    """
    A class representing a price panel in a graphical user interface.
    It inherits from the Panel class.
    
    Attributes:
        x (int): The x-coordinate of the price panel's position.
        y (int): The y-coordinate of the price panel's position.
        width (int): The width of the price panel.
        height (int): The height of the price panel.
    """
    def __init__(self,x,y,width, height):
        """
        Initializes a PricePanel object.
        
        Args:
            x (int): The x-coordinate of the price panel's position.
            y (int): The y-coordinate of the price panel's position.
            width (int): The width of the price panel.
            height (int): The height of the price panel.
        """
        super().__init__(x,y,width,height)