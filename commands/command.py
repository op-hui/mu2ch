# -*- coding: utf-8 -*-

"""
Commands

Commands describe the input the player can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia.contrib import menusystem
from evennia.server.sessionhandler import SESSIONS
from evennia.commands.default.muxcommand import MuxPlayerCommand
from evennia.utils import utils, create, search, prettytable
import time
from django.conf import settings
from evennia import create_object

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own
    command styles. Note that Evennia's default commands
    use MuxCommand instead (next in this module).

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    """
    # these need to be specified

    key = "MyCommand"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    # optional
    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    # (we don't implement hook method access() here, you don't need to
    #  modify that unless you want to change how the lock system works
    #  (in that case see evennia.commands.command.Command))

    def at_pre_cmd(self):
        """
        This hook is called before `self.parse()` on all commands.
        """
        pass

    def parse(self):
        """
        This method is called by the `cmdhandler` once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from `self.func()` (see below).

        The following variables are available to us:
           # class variables:

           self.key - the name of this command ('mycommand')
           self.aliases - the aliases of this cmd ('mycmd','myc')
           self.locks - lock string for this command ("cmd:all()")
           self.help_category - overall category of command ("General")

           # added at run-time by `cmdhandler`:

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following `self.cmdstring`.
           self.cmdset - the `cmdset` from which this command was picked. Not
                         often used (useful for commands like `help` or to
                         list all available commands etc).
           self.obj - the object on which this command was defined. It is often
                         the same as `self.caller`.
        """
        pass

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the `cmdhandler` right after `self.parser()` finishes, and so has access
        to all the variables defined therein.
        """
        self.caller.msg("Command called!")

    def at_post_cmd(self):
        """
        This hook is called after `self.func()`.
        """
        pass


class MuxCommand(default_cmds.MuxCommand):
    """
    This sets up the basis for Evennia's 'MUX-like' command style.
    The idea is that most other Mux-related commands should
    just inherit from this and don't have to implement parsing of
    their own unless they do something particularly advanced.

    A MUXCommand command understands the following possible syntax:

        name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

    The `name[ with several words]` part is already dealt with by the
    `cmdhandler` at this point, and stored in `self.cmdname`. The rest is stored
    in `self.args`.

    The MuxCommand parser breaks `self.args` into its constituents and stores them
    in the following variables:
        self.switches = optional list of /switches (without the /).
        self.raw = This is the raw argument input, including switches.
        self.args = This is re-defined to be everything *except* the switches.
        self.lhs = Everything to the left of `=` (lhs:'left-hand side'). If
                     no `=` is found, this is identical to `self.args`.
        self.rhs: Everything to the right of `=` (rhs:'right-hand side').
                    If no `=` is found, this is `None`.
        self.lhslist - `self.lhs` split into a list by comma.
        self.rhslist - list of `self.rhs` split into a list by comma.
        self.arglist = list of space-separated args (including `=` if it exists).

    All args and list members are stripped of excess whitespace around the
    strings, but case is preserved.
    """

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the `cmdhandler` right after `self.parser()` finishes, and so has access
        to all the variables defined therein.
        """
        # this can be removed in your child class, it's just
        # printing the ingoing variables as a demo.
        super(MuxCommand, self).func()



class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
    +createNPC <name>

    Creates a new, named NPC. The NPC will start with a Power of 1.
    """ 
    key = "+createnpc"
    aliases = ["+createNPC"]
    locks = "call:not perm(nonpcs)"
    help_category = "mush"

    def func(self):
        "creates the object and names it"
        caller = self.caller
        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            # may not create npc when OOC
            caller.msg("You must have a location to create an npc.")
            return
        # make name always start with capital letter
        name = self.args.capitalize()
        # create npc in caller's location
        npc = create_object("characters.Character",
                      key=name,
                      location=caller.location,
                      locks="edit:id(%i) and perm(Builders)" % caller.id)
        # announce
        message = "%s created the NPC '%s'."
        caller.msg(message % ("You", name))
        caller.location.msg_contents(message % (caller.key, name), exclude=caller)


class CmdHomeRu(Command):
    """
    move to your character's home location

    Usage:
      home

    Teleports you to your home location.
    """

    key = u"home"
    aliases = "домой"
    locks = "cmd:perm(home) or perm(Builders)"
    arg_regex = r"$"

    def func(self):
        "Implement the command"
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("У тебя нет дома!")
        elif home == caller.location:
            caller.msg("Ты и так дома!")
        else:
            caller.move_to(home)
            caller.msg("Ты вернулся домой...")

class CmdLookRu(MuxCommand):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = u"look"
    aliases = [u"l",u"lk",u"смотреть"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        args = self.args
        if args:
            # Use search to handle duplicate/nonexistant results.
            looking_at_obj = caller.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("Тут не на что смотреть!")
                return

        if not hasattr(looking_at_obj, 'return_appearance'):
            # this is likely due to us having a player instead
            looking_at_obj = looking_at_obj.character
        if not looking_at_obj.access(caller, "view"):
            caller.msg("'%s' не существует." % args)
            return
        # get object's appearance
        caller.msg(looking_at_obj.return_appearance(caller))
        # the object's at_desc() method.
        looking_at_obj.at_desc(looker=caller)

class CmdInventoryRu(Command):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = u"inventory"
    aliases = [u"i",u"инвентарь",u"и"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        "check inventory"
        items = self.caller.contents
        if not items:
            string = "У тебя ничего нет."
        else:
            table = prettytable.PrettyTable(["name", "desc"])
            table.header = False
            table.border = False
            for item in items:
                table.add_row(["{C%s{n" % item.name, item.db.desc and item.db.desc or ""])
            string = "{wУ тебя с собой:\n%s" % table
        self.caller.msg(string)

class CmdGetRu(Command):
    """
    pick up something

    Usage:
      get <obj>

    Picks up an object from your location and puts it in
    your inventory.
    """
    key = u"get"
    aliases = "взять"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "implements the command."

        caller = self.caller

        if not self.args:
            caller.msg("Что взять?")
            return
        #print "general/get:", caller, caller.location, self.args, caller.location.contents
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            return
        if caller == obj:
            caller.msg("Ты не можешь взять себя. 0_0")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("Ты не можешь это взять.")
            return

        obj.move_to(caller, quiet=True)
        caller.msg("Ты подобрал %s." % obj.name)
        caller.location.msg_contents("%s подобрал %s." %
                                        (caller.name,
                                         obj.name),
                                     exclude=caller)
        # calling hook method
        obj.at_get(caller)

class CmdDropRu(Command):
    """
    drop something

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = u"drop"
    aliases = ["положить","бросить"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "Implement command"

        caller = self.caller
        if not self.args:
            caller.msg("Что бросить?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
        obj = caller.search(self.args, location=caller,
                            nofound_string="У тебя нет %s." % self.args,
                            multimatch_string="У тебя несколько %s:" % self.args)
        if not obj:
            return

        obj.move_to(caller.location, quiet=True)
        caller.msg("Ты кладешь %s." % (obj.name,))
        caller.location.msg_contents("%s положил %s." %
                                         (caller.name, obj.name),
                                     exclude=caller)
        # Call the object script's at_drop() method.
        obj.at_drop(caller)

class CmdGiveRu(MuxCommand):
    """
    give away something to someone

    Usage:
      give <inventory obj> = <target>

    Gives an items from your inventory to another character,
    placing it in their inventory.
    """
    key = u"give"
    aliases = [u"дать",u"передать",u"отдать"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "Implement give"

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Использование: дать <объект> = <цель>")
            return
        to_give = caller.search(self.lhs, location=caller,
                                nofound_string="У тебя нет %s." % self.lhs,
                                multimatch_string="У тебя несколько %s:" % self.lhs)
        target = caller.search(self.rhs)
        if not (to_give and target):
            return
        if target == caller:
            caller.msg("Ты оставил %s у себя." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("У тебя нет %s." % to_give.key)
            return
        # give object
        caller.msg("Ты дал %s: %s." % (to_give.key, target.key))
        to_give.move_to(target, quiet=True)
        target.msg("%s дал тебе %s." % (caller.key, to_give.key))

class CmdDescRu(Command):
    """
    describe yourself

    Usage:
      desc <description>

    Add a description to yourself. This
    will be visible to people when they
    look at you.
    """
    key = u"desc"
    aliases = "я"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "add the description"

        if not self.args:
            self.caller.msg("Ты должен рассказать о себе.")
            return

        self.caller.db.desc = self.args.strip()
        self.caller.msg("Ты рассказал о себе.")

class CmdSayRu(Command):
    """
    speak as your character

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = u"say"
    aliases = ['"', "'","сказать"]
    locks = "cmd:all()"

    def func(self):
        "Run the say command"

        caller = self.caller
        talking_npc = caller.search(self.args, location=caller.location,quiet=True)

        if not talking_npc:
            
            if not self.args:
                caller.msg("Что сказать?")
                return

            speech = self.args

            # calling the speech hook on the location
            speech = caller.location.at_say(caller, speech)

            # Feedback for the object doing the talking.
            caller.msg('Ты сказал, "%s{n"' % speech)

            # Build the string to emit to neighbors.
            emit_string = '%s говорит, "%s{n"' % (caller.name,
                                                  speech)
            caller.location.msg_contents(emit_string,
                                         exclude=caller)
        else:
            for one_npc in talking_npc:
                if one_npc.db.npc:
                    obj = one_npc
                    break

            if obj:
                self.caller.msg("(Ты подходишь к %s и начинаешь разговор.)" % obj.key)
                caller.db.last_talk_with = obj.key

                # conversation is a dictionary of keys, each pointing to
                # a dictionary defining the keyword arguments to the MenuNode
                # constructor.
                conversation = obj.db.conversation
                if not conversation:
                    self.caller.msg("%s говорит: 'Нам с тобой не о чем разговаритвать'" % (obj.key))
                    return

                    # build all nodes by loading them from the conversation tree.
                menu = menusystem.MenuTree(self.caller)
                for key, kwargs in conversation.items():
                    menu.add(menusystem.MenuNode(key, **kwargs))
                menu.start()

class CmdPoseRu(Command):
    """
    strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """
    key = u"pose"
    aliases = "действие"
    locks = "cmd:all()"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        "Hook function"
        if not self.args:
            msg = "Что ты хотел сделать?"
            self.caller.msg(msg)
        else:
            msg = "%s%s" % (self.caller.name, self.args)
            self.caller.location.msg_contents(msg)

class CmdNickRu(MuxCommand):
    """
    define a personal alias/nick

    Usage:
      nick[/switches] <nickname> [= [<string>]]
      alias             ''

    Switches:
      object   - alias an object
      player   - alias a player
      clearall - clear all your aliases
      list     - show all defined aliases (also "nicks" works)

    Examples:
      nick hi = say Hello, I'm Sarah!
      nick/object tom = the tall man
      nick hi              (shows the nick substitution)
      nick hi =            (removes nick 'hi')

    A 'nick' is a personal shortcut you create for your own use. When
    you enter the nick, the alternative string will be sent instead.
    The switches control in which situations the substitution will
    happen. The default is that it will happen when you enter a
    command. The 'object' and 'player' nick-types kick in only when
    you use commands that requires an object or player as a target -
    you can then use the nick to refer to them.

    Note that no objects are actually renamed or changed by this
    command - the nick is only available to you. If you want to
    permanently add keywords to an object for everyone to use, you
    need build privileges and to use the @alias command.
    """
    key = "nick"
    aliases = ["nickname", "nicks", "@nick", "alias","ник"]
    locks = "cmd:all()"

    def func(self):
        "Create the nickname"

        caller = self.caller
        switches = self.switches
        nicks = caller.nicks.get(return_obj=True)

        if 'list' in switches:
            if not nicks:
                string = "{wНик не указан.{n"
            else:
                table = prettytable.PrettyTable(["{wТип Ника",
                                                 "{wНик",
                                                 "{wПеревод-на"])
                for nick in utils.make_iter(nicks):
                    table.add_row([nick.db_category, nick.db_key, nick.db_strvalue])
                string = "{wУказанные ники:{n\n%s" % table
            caller.msg(string)
            return
        if 'clearall' in switches:
            caller.nicks.clear()
            caller.msg("Очищены все ники.")
            return
        if not self.args or not self.lhs:
            caller.msg("Использование: nick[/switches] nickname = [realname]")
            return
        nick = self.lhs
        real = self.rhs

        if real == nick:
            caller.msg("Нет смылса задавать такой же ник...")
            return

        # check so we have a suitable nick type
        if not any(True for switch in switches if switch in ("object", "player", "inputline")):
            switches = ["inputline"]
        string = ""
        for switch in switches:
            oldnick = caller.nicks.get(key=nick, category=switch)
            if not real:
                if "=" in self.args:
                    if oldnick:
                            # clear the alias
                            string += "\nНик заменен: '{w%s{n' (-> '{w%s{n')." % (nick, oldnick)
                            caller.nicks.remove(nick, category=switch)
                    else:
                        string += "\nНик '%s' не найден, поэтому он не может быть удален." % nick
                else:
                    string += "\nНик: '{w%s{n'{n -> '{w%s{n'." % (nick, oldnick)

            else:
                # creating new nick
                if oldnick:
                    string += "\nНик '{w%s{n' замене с '{w%s{n' на '{w%s{n'." % (nick, oldnick, real)
                else:
                    string += "\nНик задан: '{w%s{n' -> '{w%s{n'." % (nick, real)
                caller.nicks.add(nick, real, category=switch)
        caller.msg(string)

class CmdAccessRu(MuxCommand):
    """
    show your current game access

    Usage:
      access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """
    key = "access"
    aliases = ["groups", "hierarchy","доступ"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        "Load the permission groups"

        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY
        string = "\n{wИерархия доступов{n (по возрастанию):\n %s" % ", ".join(hierarchy_full)
        #hierarchy = [p.lower() for p in hierarchy_full]

        if self.caller.player.is_superuser:
            cperms = "<Superuser>"
            pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.player.permissions.all())

        string += "\n{wТвой доступ{n:"
        string += "\nПерсонаж {c%s{n: %s" % (caller.key, cperms)
        if hasattr(caller, 'player'):
            string += "\nИгрок {c%s{n: %s" % (caller.player.key, pperms)
        caller.msg(string)

class CmdWhoRu(MuxPlayerCommand):
    """
    list who is currently online

    Usage:
      who
      doing

    Shows who is currently online. Doing is an alias that limits info
    also for those with all permissions.
    """

    key = "who"
    aliases = ["doing","кто"]
    locks = "cmd:all()"

    def func(self):
        """
        Get all connected players by polling session.
        """

        player = self.player
        session_list = SESSIONS.get_sessions()

        session_list = sorted(session_list, key=lambda o: o.player.key)

        if self.cmdstring == "doing":
            show_session_data = False
        else:
            show_session_data = player.check_permstring("Immortals") or player.check_permstring("Wizards")

        nplayers = (SESSIONS.player_count())
        if show_session_data:
            # privileged info
            table = prettytable.PrettyTable(["{wИмя игрока",
                                             "{wВ игре",
                                             "{wIdle",
                                             "{wУправляет",
                                             "{wКомната",
                                             "{wCmds",
                                             "{wПротокол",
                                             "{wХост"])
            for session in session_list:
                if not session.logged_in: continue
                delta_cmd = time.time() - session.cmd_last_visible
                delta_conn = time.time() - session.conn_time
                player = session.get_player()
                puppet = session.get_puppet()
                location = puppet.location.key if puppet else "None"
                table.add_row([utils.crop(player.name, width=25),
                               utils.time_format(delta_conn, 0),
                               utils.time_format(delta_cmd, 1),
                               utils.crop(puppet.key if puppet else "None", width=25),
                               utils.crop(location, width=25),
                               session.cmd_total,
                               session.protocol_key,
                               isinstance(session.address, tuple) and session.address[0] or session.address])
        else:
            # unprivileged
            table = prettytable.PrettyTable(["{wИмя игрока", "{wВ игре", "{wIdle"])
            for session in session_list:
                if not session.logged_in:
                    continue
                delta_cmd = time.time() - session.cmd_last_visible
                delta_conn = time.time() - session.conn_time
                player = session.get_player()
                table.add_row([utils.crop(player.key, width=25),
                               utils.time_format(delta_conn, 0),
                               utils.time_format(delta_cmd, 1)])

        isone = nplayers == 1
        string = "{wИгроков:{n\n%s\n%s уникальных аккаунтов%s залогинено." % (table, "Один" if isone else nplayers, "" if isone else "")
        self.msg(string)
            

"""
команда разговора с NPC

"""


class CmdTalk(Command):
    """
    talks to an npc

    Usage:
      talk

    This command is only available if a talkative non-player-character (NPC)
    is actually present. It will strike up a conversation with that NPC
    and give you options on what to talk about.
    """
    key = "talk"
    aliases = ["говорить","ск"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        "Implements the command."

        caller = self.caller

        if not self.args:
            caller.msg("Говорить с кем?")
            return
        #print "general/get:", caller, caller.location, self.args, caller.location.contents
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            return
        if caller == obj:
            caller.msg("Ты не можешь говорить сам с собой.")
            return

        # self.obj is the NPC this is defined on

        self.caller.msg("(Ты подходишь к %s и начинаешь разговор.)" % obj.key)
        caller.db.last_talk_with = obj.key

        # conversation is a dictionary of keys, each pointing to
        # a dictionary defining the keyword arguments to the MenuNode
        # constructor.
        conversation = obj.db.conversation
        if not conversation:
            self.caller.msg("%s говорит: 'Нам с тобой не о чем разговаритвать'" % (obj.key))
            return

        # build all nodes by loading them from the conversation tree.
        menu = menusystem.MenuTree(self.caller)
        for key, kwargs in conversation.items():
            menu.add(menusystem.MenuNode(key, **kwargs))
        menu.start()
