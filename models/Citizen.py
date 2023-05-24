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

    @classmethod
    def get__citizens_len(self):
        """Returns all citizens"""
        return len(Citizen.citizens)

    @classmethod
    def get_all_citizens(cls):
        """Returns a copy of the citizens dictionary"""
        return cls.citizens.copy()

    @classmethod
    def get_home(self):
        if self.home:
            return self.home.id
        return ""
        # return 0
    
    @classmethod
    def get_work(self):
        if self.work:
            return self.work.id
        return ""

    @classmethod
    def get_satisfaction(self):
        return self.satisfaction
    
