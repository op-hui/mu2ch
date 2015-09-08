# -*- coding: utf-8 -*-
from evennia import DefaultRoom

class Building(DefaultRoom):  
    def at_object_creation(self): 
        self.db.address = None
        self.db.apartment_per_floor = None
        self.db.floor_n = None

    def apartments_n(self): 
        # raise if None
        self.db.apartment_per_floor * self.db.floor_n

    pass 
    

class Hroushevka(Building):  
    def at_objecta_creation(self): 
        super(Hrushevka, self).at_object_creation() 
        self.db.apartment_per_floor = 4
        self.db.floor_n = 5

        for (i = 1; i++; i < self.db.apartment_per_floor):
