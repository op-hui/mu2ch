# -*- coding: utf-8 -*-
"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
import random
from typeclasses.objects import Object
from evennia import create_object
from django.conf import settings

class Character(DefaultCharacter):
    """
    The Character defaults to implementing some of its hook methods with the
    following standard functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room

    """
    #hands = create_object(settings.BASE_OBJECT_TYPECLASS, "hands")

    def at_object_creation(self):
        self.db.hands = create_object(settings.BASE_OBJECT_TYPECLASS, "hands")

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

        in_hands = (con for con in self.db.hands.contents if con != looker and
                                                    con.access(looker, "view"))
        thing = []
        for con in in_hands:
            key = con.get_display_name(looker)
            if con:
                thing.append(key)        
        # get description, build string
        string = "{c%s{n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            string += "%s" % desc
        if exits:
            string += "\n{wВыходы:{n " + ", ".join(exits)
        if users or things:
            string += "\n{wТы видишь:{n " + ", ".join(users + things)
        if thing:
             string += "\n{wВ руках:{n " + ", ".join(thing)
        return string


    def at_after_move(self, source_location):
        super(Character, self).at_after_move(source_location) 
        if self.location.key == (u"Сычевальня"):
            bugurts = [u"первый бугурт", u"второй бугурт"]
            self.execute_cmd("сказать " + random.choice(bugurts))

    def announce_move_from(self, destination):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.

        Args:
            destination (Object): The place we are going to.

        """
        if not self.location:
            return
        name = self.name
        loc_name = ""
        loc_name = self.location.name
        dest_name = destination.name
        string = "%s уходит из %s, направляясь в %s."
        self.location.msg_contents(string % (name, loc_name, dest_name), exclude=self)


    def announce_move_to(self, source_location):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.

        Args:
            source_location (Object): The place we came from

        """

        name = self.name
        if not source_location and self.location.has_player:
            # This was created from nowhere and added to a player's
            # inventory; it's probably the result of a create command.
            string = "Теперь у тебя есть в распоряжении %s." % name
            self.location.msg(string)
            return

        src_name = "nowhere"
        loc_name = self.location.name
        if source_location:
            src_name = source_location.name
        string = "%s пришел в %s из %s."
        self.location.msg_contents(string % (name, loc_name, src_name), exclude=self)
