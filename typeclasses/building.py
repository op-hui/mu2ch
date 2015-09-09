# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from evennia import create_object
from mudach.utils import locationTunnelDefault

class Building(DefaultRoom):  
    def at_object_creation(self): 
        self.db.desc = "Подъезд"
        self.db.address = None
        self.db.apartment_per_floor = None
        self.db.floor_n = None

    def apartments_n(self): 
        # raise if None
        self.db.apartment_per_floor * self.db.floor_n


    def build(self):
        for (i = 1; i < self.db_floor_n; i++) 
            new_floor = create_object('rooms.simpleRoom', key = "%d Этаж" % i) 
            new_floor.build(self, i) 
            localTunnelDefault(self, new_floor)
            
        
    pass 
    

class Hroushevka(Building):  
    def at_objecta_creation(self): 
        super(Hrushevka, self).at_object_creation() 
        self.db.apartment_per_floor = 4
        self.db.floor_n = 5



