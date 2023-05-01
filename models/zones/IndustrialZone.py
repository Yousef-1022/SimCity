from models.zones.Zone import Zone

class IndustrialZone(Zone):
    
    def __init__(self,x,y,mapInstance):
        super().__init__(x,y)
        self.instance = (super().createZoneObj(mapInstance))