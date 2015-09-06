# -*- coding: utf-8 -*-

"""
Commands

Commands describe the input the player can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import default_cmds

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


from evennia import Command
from evennia import create_object

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

    key = u"домой"
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

class CmdLookRu(Command):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = u"посмотреть"
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
    key = u"инвентарь"
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
    key = u"взять"
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
        caller.msg("You pick up %s." % obj.name)
        caller.location.msg_contents("%s picks up %s." %
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

    key = u"положить"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "Implement command"

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
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

class CmdGiveRu(Command):
    """
    give away something to someone

    Usage:
      give <inventory obj> = <target>

    Gives an items from your inventory to another character,
    placing it in their inventory.
    """
    key = u"дать"
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
    key = u"я"
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

    key = u"сказать"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        "Run the say command"

        caller = self.caller

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
    key = u"действие"
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