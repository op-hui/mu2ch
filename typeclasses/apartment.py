# -*- coding: utf-8 -*-
from evennia import DefaultRoom
from typeclasses.rooms import Box
from evennia import create_object
from mudach.utils import locationTunnelDefault

class BuildingApartment(Box):
    # Вход в квартиру, существует всегда
    def at_object_creation(self):
        # Номер квартиры в доме
        self.db.n = None
        # Количество "дополнительных" комнат
        self.db.additional_n = 0
        self.db.desc = u"Прихожка"

    def create_room(self, room):
        new_room = create_object('typeclasses.rooms.Box', key = room['name'])
        new_room.desc = room['desc']

        try:
            for npc in room['npc']:
                create_object(npc['typeclass'], key = npc['name'], location = new_room)
        except KeyError:
            pass

        locationTunnelDefault(self, new_room);
        return new_room
        

    def build_rooms(self): 
        i = 0 
        for i in xrange(0, len(self.rooms['default'])):
            room = self.create_room(self.rooms['default'][i])
            room.move_to(self, move_hooks = False, quiet = True)


        for i in xrange(0, min(len(self.rooms['additional']), self.db.additional_n)):
            room = self.create_room(self.rooms['additional'][i])
            room.move_to(self, move_hooks = False, quiet = True)
            
        return self

    def isUsed(self):
        return False if (self.__class__.__name__ == "BuildingApartmentUnused") else True
            

    def build(self, floor, n):
        self.db.n = n
        self.db.key = "Кв-%d" % (n) 
        self.db.floor = floor
        self.build_rooms()
        return self
        
    def __repr__(self):
        floor = self.db.floor

        if (floor):
                building = floor.getBuilding()
                return u"%s, %s, %s" % (building.name, floor.name, self.name)
        else:
                return u"об этом месте лучше не упоминать"

    def __str__(self):
        return self.__repr__() 

class BuildingApartmentUnused(BuildingApartment):
    def at_object_creation(self):
        super(BuildingApartmentUnused, self).at_object_creation()
        self.db.desc = u"Пустое нежилое помещение, ничего особенного"

    def build_rooms(self):
        pass

class BuildingApartmentUsed(BuildingApartment): 
    rooms = {
        # В непустой квартире, всегда есть эти комнаты
        "default" : [
            {
                "name" : u"Сортир",
                "desc" : u"Сортир, заметна щель ежду дверью и полом{/В углу стоит эмалированное ведро для использованной туалетой бумаги",
            },  
            {
                "name" : u"Ванная",
                "desc" : u"Ржавая ванная с капающим краном, каждый предмет в ванной исчточает совковую эпоху",
                "npc": [
                     { 
                        "typeclass": 'typeclasses.npc.YourDad',
                        "name": 'Батя',
                     } 
                 ]  
            },
            {
                "name" : u"Кухня",
                "desc" : u"Женское место, пованивает рыбой",
                "npc"  : [
                     { 
                        "typeclass": 'typeclasses.npc.YourMom',
                        "name": 'Твоя мамка',
                     } 
                 ]  
            }, 
            {
                "name" : u"Сычевальня",
                "desc" : u"Пека, открытый двач, родная капчевальня" 
            }, 
        ], 
        # Дополнительные комнаты
        "additional" : [
            {
                "name" : u"Кладовка",
                "desc" : u"Темное место"
            } 
        ] 
    } 
