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
            
    def unusedApartment(self):
        # TODO Фильтровать по типам объекта возвращаемое из contents_get()
        location = None
        for i in self.contents_get():
            try:
                location = i.unusedApartment() 
            except AttributeError:
                # лол ищем во всем подряд, даже небо, даже аллаха
                pass
            if (location):
                return location

        return None
        

    def assignApartmentToCharacter(self, apartment_location, character): 
        # TODO проверяеть тип локации который нам дают
        floor = apartment_location.db.floor

        # Уничтожаем пустую квартиру
        room_n = apartment_location.db.n
        apartment_location.delete() 
        
        # Создаем кваритру с комнатами
        new_apartment = create_object('apartment.BuildingApartmentUsed', key = apartment_location.db.key)
        new_apartment.build(floor, room_n) 
        new_apartment.db.assign_to = character
        locationTunnel(new_apartment, new_apartment.db.key, floor, u"Лестничная площадка")
        return new_apartment
        

    def assignCharacter(self, character):
        # TODO проверять аргументы
        apartment = self.unusedApartment() 
        if (apartment is not None):
            # пересоздаем хату
            apartment = self.assignApartmentToCharacter(apartment, character)
            # Хата
            character.db.flat = apartment
            print "Заселили %s в %s" % (character.db.key, apartment.db.key) 
        else:
            print "Свободных хат нет!"



    pass 
    

class Hrushevka(Building):  
    def at_object_creation(self): 
        super(Hrushevka, self).at_object_creation() 
        self.db.apartment_per_floor = 4
        self.db.floor_n = 5
        self.build() 

    pass
