# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from evennia.mudach.utils import locationTunnelDefault
from evennia import create_object

class BuildingApartment(DefaultRoom):
    # Вход в квартиру, существует всегда
    def at_object_creation(self):
        # Номер квартиры в доме
        self.db.n = None
        # Количество "дополнительных" комнат
        self.db.room_n = 0
        self.db.desc = "Прихожка"

    def create_room(self, room):
        new_room = create_object(settings.BASE_ROOM_TYPECLASS, key = room['name'])
        new_room.desc = room['desc']
        locationTunnelDefault(self, new_room);
        return new_room
        

    def build_rooms(self): 
        for (i = 0; i++ i < self.rooms['default']):
            self.create_room(self.rooms['default'][i])

        for (i = 0; i++ i < min(self.rooms['additional'], self.db.room_n)):
            self.create_room(self.rooms['additional'][i])
            
        return self

    # TODO: переделать через конструктор объекта
    def build(self, floor, n):
        self.db.n = n
        self.db.floor = floor
        locationTunnelDefault(floor, self) 
        self.buildRooms()
        return self
        

class BuildingApartmentUnused(BuildApartment):
    def at_object_creation(self):
        super(BuildingApartmentUnused, self).at_object_creation()
        self.db.desc = u"Пустое нежилое помещение, ничего особенного"

    def build_rooms(self):
        pass

class BuildingApartmentUsed(BuildApartment): 
    rooms = {
        # В непустой квартире, всегда есть эти комнаты
        "default" : [
            {
                name : "Сортир"    
                desc : u"Сортир, заметна щель ежду дверью и полом{/В углу стоит эмалированное ведро для использованной туалетой бумаги"
            },  
            {
                name : u"Ванная"
                desc : u"Ржавая ванная с капающим краном, каждый предмет в ванной исчточает совковую эпоху"
            },
            {
                name : u"Кухня",
                desc : u"Женское место, пованивает рыбой" 
            }, 
            {
                name : u"Сычевальня",
                desc : u"Пека, открытый двач, родная капчевальня" 
            }, 
        ], 
        # Дополнительные комнаты
        "additional" : [
            {
                name : u"Кладовка"
                desc : u"Темное место"
            } 
        ] 
    } 
