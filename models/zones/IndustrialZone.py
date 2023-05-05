from models.zones.Zone import Zone

class IndustrialZone(Zone):
    
    def __init__(self,x,y,creationTime,mapInstance):
        super().__init__(x,y,creationTime)
        self.price = 300
        self.instance = (super().createZoneObj(mapInstance))
        self.instance.properties['MaintenanceFee'] = 500