import os
from pytmx import TiledObject
from models.Timer import Timer

def getFilesFromDir (dir_path) -> list:
    """Returns all the files as a list from the given path"""
    return os.listdir(dir_path)

def getIconAndType (file , dir_attachment=None) -> tuple:
    """Returns a (FileLocation , ClassName) tuple"""
    parts = file.split("_")
    type = os.path.splitext(parts[1])[0]
    if (dir_attachment):
        return(dir_attachment+file,type)
    return (file,type)

def getIconLocByName (name,tuple_list) -> list:
    """Returns a list consisting of (FileLocation , ClassName) tuples"""
    return ([t[0] for t in tuple_list if name in t[0]])[0]

def addCitizen (tiledObj,citizenId):
    """Adds a citizen into the tiledObj"""
    tiledObj.properties['Citizens'].append(citizenId)
    
def removeCitizen (tiledObj,citizenId):
    """Removes a citizen from the tiledObj based on their ID"""
    tiledObj.properties['Citizens'].remove(citizenId)
    
def getOverAllSatisfaction(list:list) -> bool:
    """Returns overall satisfaction of the city"""
    res = 0
    for i in list:
        res += i.satisfaction
    return res

def hasYearPassedFromCreation(obj:TiledObject,givenDate:Timer) -> bool:
    """Checks the creation date of the zone/Building and the givenDate whether a year has passed or not """
    x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
    if x % 365 == 0:
        return True
    return False
    
def hasQuarterPassedFromCreation(obj:TiledObject,givenDate:Timer) -> bool:
    """Checks if a quarter (90 days) passed since creation"""
    x = givenDate.subtract_with_time_str(obj.properties["CreationDate"])
    if x % 90 == 0:
        return True
    return False