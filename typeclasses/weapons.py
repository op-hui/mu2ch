# -*- coding: utf-8 -*-
"""
Weapons

Наш пока простенький класс для объектов-оружия

"""

from typeclasses.objects import Object
from evennia.utils import utils, create, search, prettytable
from django.core.exceptions import ObjectDoesNotExist

from evennia import create_object
from django.conf import settings


class Weapon(Object):
    """
    Основной класс для оружия, здесь будем править return_appearence
    """
    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 0

    def return_appearance(self, looker):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
        """
        if not looker:
            return
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                                                    con.access(looker, "view"))
        exits, users, things = [], [], []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.has_player:
                users.append("{c%s{n" % key)
            else:
                things.append(key)
        # get description, build string
        string = "{c%s{n\n" % self.get_display_name(looker)
        desc = self.db.desc
        durability = self.db.durability
        if desc:
            string += "%s" % desc
        if things:
            string += "\n{wКомплектующие:{n " + ", ".join(users + things)
        if durability:
            string += "\n{wЗапас прочности: %s{n " % durability
        return string

class Knife(Weapon):

    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 1
        self.db.desc = "Картонный нож. Достосно прочный что убить кого-то... один раз."

class AcidBottle(Weapon):

    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 3
        self.db.desc = "Банка с серной кислотой. Можно облить кого-нить и наблюдать, как он подыхает."
"""
и на будущее
"""
class Pistol(Weapon):

    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 50
        self.db.desc = "Пистолет ТТ."
        mag = create_object(settings.BASE_OBJECT_TYPECLASS, "Магазин на 12 патронов", self, home=self)
        mag.db.desc = "Магазин на 12 патронов"


