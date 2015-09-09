# -*- coding: utf-8 -*-
from django.conf import settings
from evennia import create_object

from evennia import DefaultPlayer, DefaultGuest
from evennia.objects import DefaultExit
from evennia.utils import search
from utils import locationTunnelDefault


def PlayerDynamicLocation(player):
    def alreadyHas():
        return False
    def createLocation(): 

        hallway = create_object('extended_room.ExtendedRoom', key = u"Прихожка")
        hallway.db.desc = u"Сюда приходят{/Под ногами уютно поскрипывает паркет"

        anonRoom = create_object('extended_room.ExtendedRoom', key = u"Сычевальня")
        anonRoom.db.desc = u"Все облезло-обшарпано, стулья, диван древние разъебанные в хлам, ремонт утонул, разве что компьютерный стол из этого века"

        kitchen = create_object('extended_room.ExtendedRoom', key = u"Кухня")
        kitchen.db.desc = u"Женское место, пованивает рыбой"

        mom = create_object("npc.YourMom", key = "Твоя Мамка", location = kitchen)


        toilet = create_object('extended_room.ExtendedRoom', key = u"Сортир")
        toilet.db.desc = u"Сортир, заметна щель ежду дверью и полом{/В углу стоит эмалированное ведро для использованной туалетой бумаги"

        dad = create_object("npc.YourDad", key = "Лысый Батя", location = toilet)

        badroom = create_object('extended_room.ExtendedRoom', key = u"Ванная")
        badroom.db.desc = u"Ржавая ванная с капающим краном, каждый предмет в ванной исчточает совковую эпоху"


        for room in [anonRoom, kitchen, toilet, badroom]: 
            locationTunnelDefault(hallway, room)

        homeRoom = hallway

        character = player.character
        corridor = character.search(u"1-Коридор", global_search = True) 
        if (corridor): 
            create_object(settings.BASE_EXIT_TYPECLASS, u"Лестничная площадка", location = hallway, destination = corridor)
            #locationTunnelDefault(hallway, corridor)
            

        return homeRoom

    if not alreadyHas():
        return createLocation() 
    else: 
        return None
            

class Player(DefaultPlayer):
    """
    This class describes the actual OOC player (i.e. the user connecting
    to the MUD). It does NOT have visual appearance in the game world (that
    is handled by the character which is connected to this). Comm channels
    are attended/joined using this object.

    It can be useful e.g. for storing configuration options for your game, but
    should generally not hold any character-related info (that's best handled
    on the character level).

    Can be set using BASE_PLAYER_TYPECLASS.


    * available properties

     key (string) - name of player
     name (string)- wrapper for user.username
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     user (User, read-only) - django User authorization object
     obj (Object) - game object controlled by player. 'character' can also be used.
     sessions (list of Sessions) - sessions connected to this player
     is_superuser (bool, read-only) - if the connected user is a superuser

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods

     msg(text=None, **kwargs)
     swap_character(new_character, delete_old_character=False)
     execute_cmd(raw_string, sessid=None)
     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, player=False)
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hook methods (when re-implementation, remember methods need to have self as first arg)

     basetype_setup()
     at_player_creation()

     - note that the following hooks are also found on Objects and are
       usually handled on the character level:

     at_init()
     at_cmdset_get(**kwargs)
     at_first_login()
     at_post_login(sessid=None)
     at_disconnect()
     at_message_receive()
     at_message_send()
     at_server_reload()
     at_server_shutdown()

    """
    def at_pre_login(self):
        super(Player, self).at_pre_login() 
        

    def at_post_login(self, sessid = None):
        super(Player, self).at_post_login(sessid)

        
        try:
            if (settings.TEST_SERVER):
                self.permissions.add('Builders') 
        except AttributeError:
            pass


        homeLocation = PlayerDynamicLocation(self)    
        
        if (homeLocation is not None):
            character = self.character
            character.home = character.location = homeLocation
            character.move_to(homeLocation)


    pass
        



class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Players, Guests and their
    characters are deleted after disconnection.
    """
    pass
