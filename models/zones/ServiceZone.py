from models.zones.Zone import Zone
from models.Utils import remove_citizen_from_zone

class ServiceZone(Zone):
    
    price = 700
    
    def __init__(self,x,y,creationTime,mapInstance):
        super().__init__(x,y,creationTime)
        self.price = ServiceZone.price
        self.instance = (super().createZoneObj(mapInstance))
        self.instance.properties['MaintenanceFee'] = 400
        self.instance.properties['Capacity'] = 5
        
    def get_citizens_satisfaction(self) -> int:
        """Returns the satisfaction of the citizens in this Zone"""
        return sum (citizen.satisfaction for citizen in self.instance.properties['Citizens'])
    
    def remove_citizen(self,c):
        """Removes a citizen from the list"""
        remove_citizen_from_zone(c)
        