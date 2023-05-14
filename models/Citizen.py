import random

class Citizen:
    citizens = {}
    next_id = 1
    def __init__(self):
        self.home = None
        self.work = None
        self.satisfaction = random.randint(50, 100) 
        self.id = Citizen.next_id
        Citizen.next_id += 1
        Citizen.citizens[self.id] = self
    