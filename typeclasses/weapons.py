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
    durability - прочность оружия, количество убиств которое можно им совершить.
    is_weapon - флаг обозначающий, что передмет является оружием, т.е. этим пердметом можно убить.
    """
    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 0
        #и говорим что наш предмет оружие(bool)
        self.db.is_weapon = True
        #добавим часть тела, куда одевается предмет
        #self.db.placing = "RightHand"

    def return_appearance(self, looker):
        """
        Оверрайд отображения описания объекта
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
"""
класс катранного ножа
"""
    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 1
        #self.db.placing = "RightHand"
        self.db.desc = "Картонный нож. Достосно прочный что убить кого-то... один раз."

class AcidBottle(Weapon):
"""
класс банки с кислотой
"""

    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 3
        #добавим часть тела, куда одевается предмет
        #self.db.placing = "RightHand"
        self.db.desc = "Банка с серной кислотой. Можно облить кого-нить и наблюдать, как он подыхает."
"""
и на будущее
"""
class Pistol(Weapon):

    def at_object_creation(self):
        #добавляем прочность нашему оружию(int)
        self.db.durability = 50
        #добавим часть тела, куда одевается предмет
        #self.db.placing = "RightHand"
        self.db.desc = "Пистолет ТТ."
        mag = create_object(settings.BASE_OBJECT_TYPECLASS, "Магазин на 12 патронов", self, home=self)
        mag.db.desc = "Магазин на 12 патронов"


