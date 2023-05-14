import random
from models.Utils import add_citizen , simulate_building_addition

class Citizen:
    __citizens = {}
    __next_id = 1
    def __init__(self):
        self.home = None
        self.work = None
        self.satisfaction = random.randint(50, 100) 
        self.id = Citizen.__next_id
        Citizen.__next_id += 1
        Citizen.__citizens[self.id] = self
    
    @classmethod
    def get_citizen_by_id(self,id:int) -> 'Citizen':
        """Returns a Citizen object using the id"""
        return Citizen.__citizens.get(id)
    
    @classmethod
    def get_current_satisfaction(self) -> int:
        """Returns current overall satisfaction for all citizens"""
        return sum (citizen.satisfaction for citizen in Citizen.__citizens.values())
    
    @classmethod
    def get_max_possible_satisfaction(self) -> int:
        """Returns the max satisfaction possible for all created citizens"""
        return len(Citizen.__citizens) * 100
    
    @classmethod
    def get_total_citizens(self) -> int:
        """Returns the total number of citizens"""
        return len(Citizen.__citizens)
    
    @classmethod
    def get_sad_citizens(self,s_lvl:int) -> list['Citizen']:
        """
        Gets a list of citizens who have a satisfaction level
        less or equal to the given lvl

        Args:
            s_lvl: The satisfaction level the citizens should be less or equal to
            
        Returns:
            List of sad citizens  
        """
        return (c for c in Citizen.__citizens.values() if c.satisfaction <= s_lvl)
    
    def assign_to_residential_zone(self,RZone,mapInstance):
        """
        Gives the citizen a home, deletes the Citizen if there's a failure assigning a home.
        mapInstance is required to be passed in order to simulate the addition of the buildings on top of the Zone
        
        Args:
            RZone: ResidentialZone
            mapInstance : Map object
        
        Returns:
            Nothing 
        """
        if (add_citizen(RZone,self)):
            self.home = RZone
            simulate_building_addition(RZone,mapInstance)
        else:
            if(self.work):
                self.work.remove_citizen(self)
            del Citizen.__citizens[self.id]
         
    def assign_to_work_zone(self,WorkZone,mapInstance):
        """Assigns the citizen to either a ServiceZone or IndustrialZone, deletes the Citizen if there's a failure assigning work"""
        if (add_citizen(WorkZone,self)):
            self.work = WorkZone
            simulate_building_addition(WorkZone,mapInstance)
        else:
            print("Can't assign citizen cuz W_zone is full", WorkZone.properties['Capacity'])
