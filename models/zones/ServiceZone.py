from models.Zones.Zone import Zone

class ServiceZone(Zone):
    
    def __init__(self,x,y,mapInstance):
        super().__init__(x,y)
        self.instance = (super().createZoneObj(mapInstance))   
        