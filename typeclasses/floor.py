# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from typeclasses.rooms import Room
from evennia import create_object
from mudach.utils import locationTunnelDefault, locationTunnel

class BuildingFloor(DefaultRoom):
    def at_object_creation(self):
        # номер этажа
        self.db.n = None
        # связь со зданием
        self.db.building = None
        self.db.desc = "Неизвестный этаж"

    # TODO: переписать с использованием setter/getter
    def getBuilding():
        return self.db.building

    

    def build(self, building, n):
        self.db.n = n
        self.db.desc = u"%d этаж" % n
        self.db.building = building
        per_floor = building.db.apartment_per_floor
        i = 1
        for i in xrange(i, per_floor + 1):
            room_n = ((n - 1) * per_floor) + i 
            roomEntryLocation = create_object('apartment.BuildingApartmentUnused', key = u"Кв-%d" % room_n)
            roomEntryLocation.build(self, room_n) 
            locationTunnel(roomEntryLocation, roomEntryLocation.key, self, u"Лестничная площадка")
        return self

    pass
