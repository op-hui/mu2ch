# -*- coding: utf-8 -*-
from evennia import create_object
from evennia import TICKER_HANDLER as tickerhandler
from typeclasses.objects import Object

# TODO рефакторить это все дело надо
class Popustilo(Object):
    def doit(self):
        caller = self.db.caller
        substance_name = self.db.substance
        if substance_name in caller.db.effects:
            del caller.db.effects[substance_name]
            caller.msg(u"Тебя попустило с %s" % substance_name)

        tickerhandler.remove(self, self.db.affect_time)
        self.delete() 
        

class Substance(Object):
    def at_object_creation(self):
        self.db.is_substance = True
        self.db.affect_time = 60
        self.db.name = "Неизвестная субстанция"

    def use(self, caller):
        self.db.caller = caller
        caller.msg(u"%s плавно распространяется по твоему телу" % self.db.name )

        popustilo = create_object('typeclasses.substance.Popustilo', key = "Эффект от вещества %s на игроке %s" % (self.db.name, caller.name))

        popustilo.db.caller = caller
        popustilo.db.substance = self.db.name
        popustilo.db.affect_time = self.db.affect_time

        caller.db.effects[self.db.name] = popustilo

        tickerhandler.add(popustilo, self.db.affect_time, hook_key = 'doit')
        self.delete() 

class Veshestvo(Substance):
    def at_object_creation(self):
        super(Veshestvo, self).at_object_creation()
        self.db.affect_time = 300 
        self.db.name = "Вещества"
