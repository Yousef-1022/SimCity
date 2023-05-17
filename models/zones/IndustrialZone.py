from models.zones.Zone import Zone
from models.Utils import remove_citizen_from_zone

class IndustrialZone(Zone):
    
    price = 300
    
    def __init__(self,x,y,creationTime,mapInstance):
        super().__init__(x,y,creationTime)
        self.price = IndustrialZone.price
        self.instance = (super().createZoneObj(mapInstance))
        self.instance.properties['MaintenanceFee'] = 500
        self.instance.properties['Capacity'] = 10
    
    def get_citizens_satisfaction(self) -> int:
        """Returns the satisfaction of the citizens in this Zone"""
        return sum (citizen.satisfaction for citizen in self.instance.properties['Citizens'])
    
    def remove_citizen(self,c):
        """Removes a citizen from the list"""
        remove_citizen_from_zone(c)