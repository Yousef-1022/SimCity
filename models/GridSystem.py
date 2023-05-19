from models.Tile import Tile

class GridSystem:
    def __init__(self,mapInstance):
        map = mapInstance.return_map()
        self.rows = map.width
        self.cols = map.height
        self.matrix = [[None for j in range(self.cols)] for i in range(self.rows)]
        for layer in map.visible_layers:
            if layer.name == "Objects" or layer.name == "ObjectsTop":
                continue
            for x, y, gid in layer:
                if (layer.name == "Water" or layer.name == "WaterEdges") and not (gid == 0):
                    t = Tile(x,y,"Water",True)
                    self.matrix[x][y] = t
                elif not (gid == 0):
                    t = Tile(x,y,"Ground",False)
                    self.matrix[x][y] = t


