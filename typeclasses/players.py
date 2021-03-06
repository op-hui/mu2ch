# -*- coding: utf-8 -*-
from django.conf import settings
from evennia import create_object

from evennia import DefaultPlayer, DefaultGuest
from evennia.objects import DefaultExit
from evennia.utils import search
from utils import locationTunnelDefault, locationTunnel


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

        character = self.character
        
        # Вероятно, этот код нужно убрать в at_first_login хук
        try:
            homeLocation = character.search(u"1-Общий дворик", global_search = True, quiet = True)[0] 
        except IndexError:
            # сервер после вайпа, нужно выполнить инцилизацию локаций вручную
            # bathccommand mu2ch_init
            # пока заглушка
            return 

        if (homeLocation and character.home != homeLocation):
            character.home = character.location = homeLocation
            character.move_to(homeLocation)
        
    
        apartment = None

        if (character.db.flat):
            return 

        i = 1
        while (apartment is None):
            try:
                building = character.search(u"1-Дом%d" % i, global_search = True, quiet = True)[0] 
            except IndexError:
                try:
                    building_home = character.search(u"Преддомовая территория", global_search = True, quiet = True)[0]
                except IndexError:
                    # что то пошло не так
                    return

                building = create_object('typeclasses.building.Hrushevka', key = u"Дом%d" % i) 
                locationTunnel(building, u"Дом%d" % i , building_home, u"Улица")
                if (not building):
                    print "Что-то пошло не так"
                    # never happend
                    break

            # db.flat - локация хаты персонажа
            apartment = building.assignCharacter(character) 
            if (apartment): 
                character.msg("Тебя заселили по адресу: %s" % repr(apartment)) 

            i = i + 1

    pass
        



class Guest(DefaultGuest):
    """
    This class is used for guest logins. Unlike Players, Guests and their
    characters are deleted after disconnection.
    """
    pass
