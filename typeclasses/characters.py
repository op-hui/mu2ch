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
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import delay

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
    #религии
    avaible_religions = ["христианство","буддизм","сатанизм"]

    def at_object_creation(self):
        #прикручиваем руку
        self.db.hands = create_object(settings.BASE_OBJECT_TYPECLASS, "hands")
        #прикручиваем фраги
        self.db.frags = 0
        #прикручиваем количество смертей
        self.db.death_count = 0
        #прикручиваем массив ээфектов
        self.db.effects = []
        # ассоциация с хатой.
        self.db.flat = None
        #прикручивам группу
        self.db.party = []
        #прикручиваем лидера группы
        self.db.party_leader = None
        #прикручиваем деньги
        self.db.money = 100
        #прикручиваем религию
        self.religion = "атэист"

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
        #обоработка группы
        party = self.db.party
        if party:
            for member in party:
                player = self.search(member, global_search=True,nofound_string="Сорпатиец %s не найден!" % member)
                if not player:
                    return
                if player and player.has_player:
                    player.location.msg_contents("%s последовал за лидером %s" % (player.key, self.key))
                    player.move_to(self.location,quiet=True)
                    player.msg("Ты полследовал за лидером - %s. Вы отправились в %s" % (self.key, self.location.name))


    def at_die(self):
        """
        хук смерти игрока. создает труп, скидывает в него вещи, переносит игрока в лимб.
        """
        #создаем труп
        corpse = create_object(Corpse,self.key, location=self.location)
        #corpse.key = "Труп %s" % self.key
        descriptions = ["Изуродованный труп %s" % self.key,
                        "Бренное тело %s" % self.key,
                        "Останки %s" % self.key,
                        "Все, что оcталось от %s" % self.key]
        corpse.db.desc = random.choice(descriptions)
        #скидываем внего вещи
        items = self.contents
        if items:
            for item in items:
                item.move_to(corpse, quiet=True)
        if self.db.hands:
            in_hands = self.db.hands.contents
            if in_hands:
                item = in_hands[0]
                item.move_to(corpse,quiet=True)
        #сбарсываем пати, если ты умер, или умер лидер
        leader = self.db.party_leader
        party = self.db.party
        
        if party:
            for member in party:
                player = self.search(member, global_search=True,nofound_string="Сорпатиец %s не найден!" % member)
                if not player:
                    return
                player.db.party_leader = None
                player.msg("Ваш лидер погиб и ваша группа распалась.")
            self.db.party = []
            self.msg("Твоя группа распалась.")

        if leader:
            your_leader = self.search(leader, global_search=True,nofound_string="Лидер %s не найден!" % leader)
            your_leader.db.party.remove(self.key)
            your_leader.msg("%s погиб и вышел и твой группы." % self.key)
            self.db.party_leader = None
            self.msg("Ты покинул группу %s" % your_leader.key)

        # задрежка
        delay(5, callback=self.TelToLimb)

    def TelToLimb(self):
        #телепортируем персонажа в лимб
        #limbs = self.search("Limbo", global_search=True, quiet=True,nofound_string="Бога нет, и рая нет!" )
        limbs = self.search(True, global_search=True, attribute_name = 'after_death', quiet=True,nofound_string="Бога нет, и рая нет!" )


        if limbs:
            limb = limbs[0]
            self.move_to(limb, quiet=True)
        else:
            self.msg("Ты не смог попасть в рай. Потому что его нет! Где твой Бог теперь?")



class Corpse(Character):
    """
    Класс трупа игрока. Будет создаваться когда игрок умирает и исчезать через 3 минуты.
    """
    def at_object_creation(self):
        self.db.is_corpse = True
        self.db.hands = create_object(settings.BASE_OBJECT_TYPECLASS, "hands")
        #создаем таймер для трупа
        tickerhandler.add(self, 60*3)
    def at_tick(self):
        #уничтожает все свои вещи и самовыпиливается
        self.location.msg_contents("Прах игрока %s исчезает у тебя на глазах" % self.key)
        items = self.contents
        if items:
            for item in items:
                item.delete()
        self.delete()

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
        if self.db.hands:
            in_hands = (con for con in self.db.hands.contents if con != looker and
                                                        con.access(looker, "view"))
            thing = []
            for con in in_hands:
                key = con.get_display_name(looker)
                if con:
                    thing.append(key)        
        # get description, build string
        string = "{C%s{n\n" % self.get_display_name(looker)
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
