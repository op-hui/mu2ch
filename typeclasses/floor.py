# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from evennia import create_object
from mudach.utils import locationTunnelDefault, locationTunnel

class BuildingFloor(DefaultRoom):
    def at_object_creation(self):
        # номер этажа
        self.db.n = None
        # связь со зданием
        self.db.building = None
    

    # TODO: переписать с использованием setter/getter
    # Возвращает локацию здания
    def getBuilding():
        # XXX заглушка
        return self.db.building

    

    # TODO переделать через конструктор объекта
    def build(self, building, n):
        self.db.n = n
        self.db.building = building
        per_floor = building.db.apartment_per_floor
        i = 0
        for i in xrange(i, per_floor):
            roomEntryLocation = create_object('apartment.BuildingApartmentUnused', key = "Кв-%d" % (n * per_floor + i))
            locationTunnel(roomEntryLocation, "Лестничная площадка", self, roomEntryLocation.key)
        return self

    pass