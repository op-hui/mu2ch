# -*- coding: utf-8 -*-
"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from django.core.exceptions import ObjectDoesNotExist
from mudach.utils import isCharacter


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

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
            elif con.db.npc:
                things.append("{y%s{n" % key)
            else:
                things.append(key)
        # get description, build string
        string = "{c%s{n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            if self.db.details :
                for detail in self.db.details.keys():
                    det = desc.count(detail)
                    if det > 0:
                        desc = desc.replace(detail,"{y%s{n" % detail)
            string += "%s" % desc
        if exits:
            string += "\n{wВыходы:{n " + ", ".join(exits)
        if users or things:
            string += "\n{wТы видишь:{n " + ", ".join(users + things)
        return string

    pass

# Этот класс при удалении рекурсивно удаляет все кроме игроков
class Box(DefaultRoom):

    def at_object_delete(self):
        print "Комната удалена %s" % self.key
        for i in self.contents_get():
            try:
                if (not isCharacter(i)):                
                    i.delete() 
            # XXX bug?
            except ObjectDoesNotExist:
                pass 

        return True
    pass

