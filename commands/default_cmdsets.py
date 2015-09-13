# -*- coding: utf-8 -*-
"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from typeclasses.extended_room import CmdExtendedLook,CmdExtendedDesc,CmdGameTime
from commands.help_ru import CmdHelp_ru,CmdUnconnectedHelp_ru
from commands.command import CmdCreateNPC,CmdHomeRu,CmdLookRu,CmdInventoryRu,CmdGetRu,CmdDropRu,CmdGiveRu,CmdSayRu,CmdPoseRu,CmdDescRu,CmdTalk,CmdWhoRu,CmdAccessRu,CmdNickRu
from commands.command import CmdWear,CmdUnWear,CmdGetHands,CmdMethod,CmdKill
from evennia.commands.default.muxcommand import MuxCommand
from django.conf import settings

import re
import traceback
from evennia.players.models import PlayerDB
from evennia.server.models import ServerConfig
from evennia.objects.models import ObjectDB
from evennia.utils import create, logger, utils
from evennia.commands.default.unloggedin import _create_player, _create_character

MULTISESSION_MODE = settings.MULTISESSION_MODE

class CmdUnconnectedCreateRu(MuxCommand):
    """
    create a new player account

    Usage (at login screen):
      create <playername> <password>
      create "player name" "pass word"

    This creates a new player account.

    If you have spaces in your name, enclose it in quotes.
    """
    key = u"создать"
    aliases = ["cre", "cr"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"

    def func(self):
        "Do checks and create account"

        session = self.caller
        args = self.args.strip()

        # extract quoted parts
        parts = [part.strip() for part in re.split(r"\"|\'", args) if part.strip()]
        if len(parts) == 1:
            # this was (hopefully) due to no quotes being found
            parts = parts[0].split(None, 1)
        if len(parts) != 2:
            string = u"\n Использование (без <>): создать <имя персонажа> <пароль>" \
                     u"\nЕсли <имя персонажа> или <пароль> содержат пробелы, нужно взять их в ковычки"
            session.msg(string)
            return
        playername, password = parts

        # sanity checks
        if not re.findall('^[\w. @+-]+$', playername) or not (0 < len(playername) <= 30):
            # this echoes the restrictions made by django's auth
            # module (except not allowing spaces, for convenience of
            # logging in).
            string = u"\n\r Имя персонажа не должно превышать 30 символов. Имя может содержать только, буквы пробелы, цифры и @/./+/-/_"
            #string = "\n\r Playername can max be 30 characters or fewer. Letters, spaces, digits and @/./+/-/_ only."
            session.msg(string)
            return
        # strip excessive spaces in playername
        playername = re.sub(r"\s+", " ", playername).strip()
        if PlayerDB.objects.filter(username__iexact=playername):
            # player already exists (we also ignore capitalization here)
            session.msg(u"Игрок с таким именем '%s' уже есть." % playername)
            return
        # Reserve playernames found in GUEST_LIST
        if settings.GUEST_LIST and playername.lower() in map(str.lower, settings.GUEST_LIST):
            string = u"\n\r Это имя зарезервировано. Пожалуйста выберите другое имя."
            session.msg(string)
            return
        if not re.findall('^[\w. @+-]+$', password) or not (3 < len(password)):
            string = u"\n\r Пароль должен быть больше трех символов и может состоять только из пробелов, цифр @\.\+\-\_"  \
                     u"\nДля лучшей безопасности выберите пароль от 8 символов " 
            session.msg(string)
            return

        # Check IP and/or name bans
        bans = ServerConfig.objects.conf("server_bans")
        if bans and (any(tup[0]==playername.lower() for tup in bans)
                     or
                     any(tup[2].match(session.address) for tup in bans if tup[2])):
            # this is a banned IP or name!
            string = u"{rТы забанен{x"
            session.msg(string)
            session.execute_cmd("quit")
            return

        # everything's ok. Create the new player account.
        try:
            permissions = settings.PERMISSION_PLAYER_DEFAULT
            typeclass = settings.BASE_CHARACTER_TYPECLASS
            new_player = _create_player(session, playername, password, permissions)
            if new_player:
                if MULTISESSION_MODE < 2:
                    default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
                    _create_character(session, new_player, typeclass,
                                    default_home, permissions)
                # tell the caller everything went well.
                string = u"Новый аккаунт создан Добро пожаловать %%USERNAME%%"
                if " " in playername:
                    string += u"\n\nТеперь можно войти в игру 'connect \"%s\" <пароль>'."
                else:
                    string += u"\n\nТеперь можно войти в игру 'connect %s <пароль>'."
                session.msg(string % (playername))

        except Exception:
            # We are in the middle between logged in and -not, so we have
            # to handle tracebacks ourselves at this point. If we don't,
            # we won't see any errors at all.
            string = u"%s\nСлучилась проблема, чиним."
            session.msg(string % (traceback.format_exc()))
            logger.log_errmsg(traceback.format_exc())



class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdCreateNPC())
        self.add(CmdHomeRu())
        self.add(CmdLookRu())
        self.add(CmdInventoryRu())
        self.add(CmdGetRu())
        self.add(CmdDropRu())
        self.add(CmdGiveRu())
        self.add(CmdDescRu())
        self.add(CmdSayRu())
        self.add(CmdPoseRu())
        self.add(CmdTalk())
        self.add(CmdHelp_ru())
        self.add(CmdExtendedLook())
        self.add(CmdExtendedDesc())
        self.add(CmdGameTime())
        self.add(CmdWhoRu())
        self.add(CmdAccessRu())
        self.add(CmdNickRu())
        self.add(CmdWear())
        self.add(CmdUnWear())
        self.add(CmdGetHands())
        self.add(CmdMethod())
        self.add(CmdKill())
        

class PlayerCmdSet(default_cmds.PlayerCmdSet):
    """
    This is the cmdset available to the Player at all times. It is
    combined with the `CharacterCmdSet` when the Player puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultPlayer"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(PlayerCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdUnconnectedHelp_ru())
        self.add(CmdUnconnectedCreateRu())


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
