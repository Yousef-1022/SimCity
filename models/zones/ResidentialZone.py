from models.zones.Zone import Zone

class ResidentialZone(Zone):
    
    def __init__(self,x,y,creationTime,mapInstance):
        super().__init__(x,y,creationTime)
        self.price = 100
        self.instance = (super().createZoneObj(mapInstance))
        self.instance.properties['MaintenanceFee'] = 200
        