# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from typeclasses.rooms import Box
from evennia import create_object
from mudach.utils import locationTunnelDefault,locationTunnel

class Building(Box):  
    def at_object_creation(self): 
        self.db.desc = u"Подъезд"
        self.db.address = None
        self.db.apartment_per_floor = None
        self.db.floor_n = None

    def apartments_n(self): 
        # raise if None
        self.db.apartment_per_floor * self.db.floor_n

    def build(self):
        i = 0
        prev_floor = None
        for i in xrange(1, self.db.floor_n):  
            new_floor = create_object('floor.BuildingFloor', key = u"%d Этаж" % i) 
            new_floor.build(self, i) 

            new_floor.move_to(self) 
                
            locationTunnel(self, self.db.desc, new_floor, None)
            if (prev_floor):
                locationTunnelDefault(prev_floor, new_floor)
            prev_floor = new_floor
            
    def searchFreeLocation():
        for i in self.contents_get():
            #floor.searchFreeLocation() 
            location = i.searchFreeLocation() 
            if (location):
                return location

        return None
        
    pass 
    

class Hrushevka(Building):  
    def at_object_creation(self): 
        super(Hrushevka, self).at_object_creation() 
        self.db.apartment_per_floor = 4
        self.db.floor_n = 5
        self.build() 
