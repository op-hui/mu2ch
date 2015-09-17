# -*- coding: utf-8 -*-
from evennia import TICKER_HANDLER as tickerhandler
from typeclasses.objects import Object

class Substance(Object):
    def at_object_creation(self):
        self.db.is_substance = True
        self.db.affect_time = 60

    def func(self):
        pass

    def use(self, caller):
        self.db.caller = caller
        tickerhandler.add(self, 10)

    def at_tick(self):
        self.func()
        tickerhandler.remove(self, self.ndb.affect_time)
        self.db.caller.msg(u"Ушла любовь, завяли помидоры") 

class Veshestvo(Substance):
    def at_object_creation(self):
        super(Veshestvo, self).at_object_creation()
        self.db.affect_time = 5

    def func(self):
        caller = self.db.caller
        caller.msg(u"Эффект") 
