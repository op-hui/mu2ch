# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from typeclasses.rooms import Box
from evennia import create_object
from mudach.utils import locationTunnelDefault, locationTunnel

class BuildingFloor(Box):
    def at_object_creation(self):
        # номер этажа
        self.db.n = None
        # связь со зданием
        self.db.building = None
        self.db.desc = "Неизвестный этаж"

    # TODO: переписать с использованием setter/getter
    def getBuilding():
        return self.db.building


    def unusedApartment(self):
        for i in self.contents_get(): 
        # TODO Фильтровать по типам объекта возвращаемое из contents_get()
                try:
                        if (i.isUsed() == False):
                                return i
                except AttributeError:
                        # лол ищем во всем подряд, даже небо, даже аллаха
                        pass

        return None
    

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
            roomEntryLocation.move_to(self)
            locationTunnel(roomEntryLocation, roomEntryLocation.key, self, u"Лестничная площадка")
        return self

    pass
