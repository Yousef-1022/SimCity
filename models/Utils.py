import os

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