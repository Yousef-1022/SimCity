from Utils import addCitizen
from models.zones import ResidentialZone

next_citizen_id = 0
class Citizen:
    def __init__(self):
        global next_citizen_id
        
        self.satisfaction = 100 
        self.home = 0
        self.work = 0
        self.id = next_citizen_id
        next_citizen_id += 1
        
    def assignToResidentialZone(self,RZone:ResidentialZone):
        """Gives the citizen a home"""
        self.home = RZone.id
        addCitizen(RZone,self.id)
         
    def assignToWorkZone(self,WorkZone):
        """Assigns the citizen to either a ServiceZone or IndustrialZone"""
        self.work = WorkZone.id
        addCitizen(WorkZone,self.id)