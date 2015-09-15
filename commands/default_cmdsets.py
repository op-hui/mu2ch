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
from commands.help_ru import CmdHelp_ru
from commands.Unloggedin_ru import CmdUnconnectedHelp_ru, CmdUnconnectedConnectRu, CmdUnconnectedCreateRu
from commands.command import CmdHomeRu,CmdLookRu,CmdInventoryRu,CmdGetRu,CmdDropRu,CmdGiveRu,CmdSayRu,CmdPoseRu,CmdDescRu,CmdTalk,CmdWhoRu,CmdAccessRu,CmdNickRu

from commands.command import CmdWear,CmdUnWear,CmdGetHands,CmdMethod,CmdKill,CmdStatus,CmdAlchemy,CmdOut,CmdFollow,CmdKikcFromParty

from evennia.commands.default.muxcommand import MuxCommand
from django.conf import settings

import re
import traceback
from evennia.players.models import PlayerDB
from evennia.server.models import ServerConfig
from evennia.objects.models import ObjectDB
from evennia.utils import create, logger, utils
from evennia.commands.default.unloggedin import _create_player, _create_character


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
        self.add(CmdStatus())
        self.add(CmdAlchemy())
        self.add(CmdOut())
        self.add(CmdKikcFromParty())
        self.add(CmdFollow())
        

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
        self.add(CmdUnconnectedConnectRu())


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
