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
import re
from django.conf import settings
from evennia import create_object
from typeclasses.alchemy import Alchemy
from evennia.utils.evmenu import get_input 
from evennia import utils

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


class CmdMethod(Command):
    """
    Вызывает и показывает результат выполнения метода у игрового объекта
    
    Использование:
        @method [obj.].methodName()

    Например:
        @method Этаж.freeRooms() # Вызов у объекта Этаж метод freeRoms()
        @method isUsed() # Если объект не указан, вызов метода isUsed происходит для текущей локации
    """

    key = "@method"
    locks = "call:perm(Immortals)"
    help_category = "Admin"

    def func(self): 
        #super(CmdMethod, self).parser()
        self.arglist = self.args.strip().split(".", 1)

        args_n = len(self.arglist)

        obj = None
        if (args_n == 2):
            # method Object.method()
            obj = self.caller.search(self.arglist[0], location = self.caller.location)
            if (obj is None):
                self.caller.msg("Такого объекта в этой локации нет")
                return False

            method = self.arglist[1]
        elif(args_n == 1):
            # method method()
            # Запускаем в текущем контексте локации
            obj = self.caller.location
            method = self.arglist[0]
        else:
            self.caller.msg(u"Используй: method объект.имя_метода(аргументы)")
            return False

        try:
            self.caller.msg(u"Output: %s" % repr(eval("obj." + method)))
        except AttributeError:
            self.caller.msg(u"Что-то пошло не так, уже чиним")
            raise 

        return True

class CmdStatus(Command):
    """
    Показывает статус персонажа
    
    Использование:
        статус

    """
    key = u"статус"
    aliases = [u"status"]

    def func(self):
        caller = self.caller
        apartment = caller.db.flat
        if (apartment):
            apartment_txt = repr(apartment) 
        else:
            apartment_txt = u"Бомж"

        message = u"""Хуй обыкновенный
    Прописка по адресу: %s
    Фрагов: %d
    Смертей: %d
    Религия: %s
    Деньги: %d (интернеты)
""" % (apartment_txt, caller.db.frags, caller.db.death_count, caller.db.religion, caller.db.money) 
    
        if caller.db.effects:

            if (len(caller.db.effects.keys())): 
                message += "    Ты находишься под воздействием: "
                for effect in caller.db.effects.keys():
                    message += effect + " "

        caller.msg(message)



        if caller.db.party_leader:
            party_leader = caller.search(caller.db.party_leader, location=caller.location, global_search=True,nofound_string="Такого игрока нет.")
            
            message = """\nГруппа:
    Лидер: %s
    """ % (party_leader.key)

            if party_leader.db.party:
                
                message+= """Сопартийцы: """
                
                for member in party_leader.db.party:
                    if member != caller.key:
                        message+="%s, " % member
                
                caller.msg(message)

        if caller.db.party:

            message = """\nГруппа:
    Ты лидер группы
    """

            message+= """Сопартийцы: """
            
            for member in caller.db.party:
                message+="%s, " % member
            
            caller.msg(message)

# TODO вероятно команду надо переменовать
# использовать можно не только вещества, но у другие предметы
class CmdUse(Command): 
    """
    Употребляешь вещество (оно должно находиться в инвентаре)
    
    Использование:
        употребить <вещество в инвентаре>

    Употребляешь вещества
    """

    key = u"употребить"
    aliases = ["use", u"юзать"]

    def func(self):
        caller = self.caller
        args = self.args

        if (not len(args)):
            caller.msg(u"Не указано какое вещество употребить.")
            return False
            
        substance = caller.search(args, location=caller, global_search = False, nofound_string = u"Такого вещества у тебя нет") 

        if (not substance):
            return False

        if (utils.inherits_from(substance, 'typeclasses.substance.Substance')):
            caller.msg(u"Ты употребил %s" % substance.name)
            substance.use(caller) 
        else:
            # TODO переработать, использовать можно не только вещества
            caller.msg(u"Ты не можешь употребить %s" % substance.name) 


        return True
        

class CmdHomeRu(Command):
    """
    move to your character's home location

    Usage:
      home

    Teleports you to your home location.
    """

    key = u"home"
    aliases = [u"домой"]
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
    aliases = [u"l",u"lk",u"смотреть",u"см"]
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

class CmdGetRu(MuxCommand):
    """
    pick up something

    Usage:
      get <obj> = <obj>

    Picks up an object from your location and puts it in
    your inventory.
    """
    key = u"get"
    aliases = [u"взять",u"брать"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "implements the command."

        caller = self.caller

        lhs = self.lhs
        rhs = self.rhs

        if not lhs:
            caller.msg("Что взять? Использование(без <>): \n взять <объект> \n взять <объект> = <объект>")
            return
        
        if not rhs:
            #print "general/get:", caller, caller.location, self.args, caller.location.contents
            obj = caller.search(lhs, location=caller.location, nofound_string = "Здесь этого нет.")
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
            caller.location.msg_contents("%s подобрал %s." % (caller.name, obj.name),exclude=caller)
            # calling hook method
            obj.at_get(caller)
            return
        
        if rhs:
            storage_arg = lhs
            obj_arg = rhs
            storage = caller.search(storage_arg, nofound_string="Здесь нет таких объектов-хранилищ.")
            
            if not storage:
                return
            
            if not (storage.db.is_corpse or storage.db.is_storage):
                caller.msg("Ты можешь обыскивать только трупы и хранилища.")
                return
            
            if (not storage.contents and not storage.db.money and storage.db.money == 0 ) :
                caller.msg("Здесь ничего нет.")
                return

            if obj_arg == "все":
                
                all_obj = storage.contents

                if storage.db.money:
                    if storage.db.money > 0:
                        caller.db.money = caller.db.money + storage.db.money
                        caller.msg("Ты взял %d интернетов." % storage.db.money)
                        storage.db.money = 0

                string = "Ты взял все, что было в %s: " % storage.key
                
                for obj in all_obj:
                    obj.move_to(caller, quiet=True)
                    string+="%s," % obj.key
                    obj.at_get(caller)
                
                caller.msg(string)
                caller.location.msg_contents("%s полностью обобрал %s" % (caller.key, storage.key),exclude=caller)
                # calling hook method
                #obj.at_get(caller)
                return

            if "деньги" in obj_arg:
               
                money_args = obj_arg.strip().split()

                if storage.db.money:
                    if storage.db.money > 0:
                        if len(money_args) == 1:
                            caller.db.money = caller.db.money + storage.db.money
                            caller.msg("Ты взял %d интернетов." % storage.db.money)
                            storage.db.money = 0
                            return
                        if len(money_args) == 2:
                            amount = int(money_args[1])
                            caller.db.money = int(caller.db.money) + amount
                            caller.msg("Ты взял %d интернетов." % amount)
                            storage.db.money = int(storage.db.money) - amount
                            return
                    else:
                        caller.msg("Здесь нет денег.")
                        return
                else:
                    caller.msg("Здесь нет денег.")
                    return

            if (not "деньги" in obj_arg and obj_arg != "все"):
                
                obj = caller.search(obj_arg, location=storage, nofound_string="Здесь нет таких объектов.")

                if not obj:
                    return

                obj.move_to(caller, quiet=True)
                caller.msg("Ты взял %s из %s" % (obj.name, storage.key))
                caller.location.msg_contents("%s забрал %s из %s." % (caller.name, obj.name,storage.key),exclude=caller)
                # calling hook method
                obj.at_get(caller)
                return



class CmdDropRu(Command):
    """
    drop something

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = u"drop"
    aliases = [u"бросить",u"выкинуть"]
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
        caller.msg("Ты выбросил %s." % (obj.name,))
        caller.location.msg_contents("%s выбросил %s." %
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
    aliases = [u"дать",u"передать",u"положить"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "Implement give"

        caller = self.caller

        if not self.args or not self.rhs:
            caller.msg("Использование: дать <объект> = <цель>")
            return

        target = caller.search(self.rhs,nofound_string="Здесь нет такой цели.")

        if not target:
            return
        
        if "деньги" in self.lhs:
            
            money_args = self.lhs.strip().split()
            
            if caller.db.money:
                if caller.db.money > 0:
                    if not target.db.money:
                        caller.msg("Ты не можешь положить или передать денньги этому объекту.")
                        return
                    if len(money_args) == 1:

                        target.db.money = target.db.money + caller.db.money
                        if (target.db.is_storage or target.db.is_corpse):
                            caller.msg("Ты положил все свои интернеты в: %s." % target.key)
                        else:
                            caller.msg("Ты отдал все свои интернеты: %s." % target.key)
                        caller.db.money = 0
                        return
            
                    if len(money_args) == 2:

                        amount = int(money_args[1])
                            
                        if int(caller.db.money) < amount:
                            caller.msg("У тебя нет такой суммы. У тебя всего %d интренетов." % caller.db.money)
                            return

                        target.db.money = int(target.db.money) + amount
                        if (target.db.is_storage or target.db.is_corpse):
                            caller.msg("Ты положил %d интернетов в: %s." % (amount, target.key))
                        else:
                            caller.msg("Ты дал %d интернетов: %s." % (amount, target.key))
                        caller.db.money = int(caller.db.money) - amount
                        return
                else:
                    caller.msg("У тебя нет денег.")
                    return
            else:
                caller.msg("У тебя нет денег.")
                return

        to_give = caller.search(self.lhs, location=caller,
                                nofound_string="У тебя нет %s." % self.lhs,
                                multimatch_string="У тебя несколько %s:" % self.lhs)

        
        if not (to_give and target):
            return
        
        if target == caller:
            caller.msg("Ты оставил %s у себя." % to_give.key)
            return
        
        if not to_give.location == caller:
            caller.msg("У тебя нет %s." % to_give.key)
            return
        
        # give object
        if (target.db.is_storage or target.db.is_corpse):
            caller.msg("Ты положил %s: %s." % (to_give.key, target.key))
        else:
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
    aliases = [u"я"]
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
    aliases = [u"действие"]
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
                location = puppet.location.key if puppet and puppet.location else "None"
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

class CmdWear(Command):
    """
    Команда для перемещения предметов в руку
    """
    key = "wear"
    aliases = [u"одеть"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller

        if not self.args:
            caller.msg("Что надеть?")
            return

        obj = caller.search(self.args, location=caller)
        
        if not obj:
            caller.msg("У тебя с собой нет %s" % self.args)
            return
        
        in_hands = caller.db.hands.contents
        if in_hands:
            string = "У тебя в руках был "
            in_hands_obj = in_hands[0]
            string+="%s, " % in_hands_obj.key
            in_hands_obj.move_to(caller, quiet=True)
            obj.move_to(caller.db.hands,quiet=True)
            string+="ты заменил это на %s." % obj.key
            caller.msg(string)
            return
        else:
            obj.move_to(caller.db.hands,quiet=True)
            caller.msg("Ты взял в руки %s" % obj.key)

class CmdUnWear(Command):
    """
    Команда для изъятия объектов их рук
    """
    key = "unwear"
    aliases = [u"снять"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller

        in_hands = caller.db.hands.contents

        if not in_hands:
            caller.msg("У тебя в руках ничего нет")
            return
        else:
            for in_hands_obj in in_hands:
                in_hands_obj.move_to(caller,quiet=True)
                caller.msg("Ты убрал из рук : %s" % in_hands_obj.key)

class CmdGetHands(Command):
    """
    Команда для изъятия объектов их рук
    """
    key = "@hands"
    aliases = ["u@руки"]
    locks = "cmd:perm(Builders)"
    help_category = "Building"

    def func(self):

        caller = self.caller

        if caller.db.hands:
            caller.msg("У тебя уже есть руки")
        else:
            caller.db.hands = create_object(settings.BASE_OBJECT_TYPECLASS, "hands")
            caller.msg("Теперь у тебя есть руки")

        if caller.db.frags:
            caller.msg("У тебя уже есть параметр фрагов")
        else:
            caller.db.frags = 0
            caller.msg("Теперь у тебя есть фраги")

        if caller.db.death_count:
            caller.msg("У тебя уже есть параметр смертей")
        else:
            caller.db.death_count = 0
            caller.msg("Теперь у тебя есть количество смертей")

        if caller.db.effects:
            caller.msg("У тебя уже есть массив с эффектами")
        else:
            caller.db.effects = []
            caller.msg("Теперь у тебя есть массив с эффектами")

class CmdOut(Command):
    """
        По этой команде персонаж выходит из локации в первый выход
        Использование:
            уйти
        
    """

    key = "уйти"
    aliases = ["out"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller
        location = self.caller.location

        caller.move_to(location.exits[0])


class CmdKill(Command):
    """
    Команда для изъятия объектов их рук
    """
    key = "kill"
    aliases = [u"убить"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller

        if caller.location.db.no_kill:
            caller.msg("Это PVE зона. Здесь нельзя убивать.")
            return

        if not self.args:
            caller.msg("Кого убиваем?")
            return

        target = caller.search(self.args, location=caller.location,nofound_string = "Нет такого игрока")

        if not target:
            return

        #if caller.location.key == "Limbo"
        #    caller.msg("Здесь нельзя убивать.")
        #    return

        if not caller.db.hands:
            caller.msg("Ты инвалид. У тебя нет рук.")
            return

        in_hands = caller.db.hands.contents

        if not target.has_player:
            caller.msg("Ты можешь убивать только игроков!")
            return

        if not in_hands:
            caller.msg("У тебя в руках ничего нет. В руках должно быть оружие!")
            return

        in_hands_obj = in_hands[0]

        if not in_hands_obj.db.is_weapon:
            caller.msg("Тем что у тебя в руках нельзя убить. В руках должно быть оружие!")
            return

        weapon = in_hands_obj   
        caller.db.frags = caller.db.frags + 1
        target.db.death_count = target.db.death_count +1
        target.db.effects = []
        if not target == caller: 
            target.msg("Тебя убил %s. Ты потерял все свои вещи и оправляешься в..." % caller.key)
            caller.msg("Ты убил %s. Теперь можешь обыскать его труп в поисках чего-нибудь ценного." % target.key)
            caller.location.msg_contents("%s убил %s." % (caller.key, target.key),exclude=caller)
        else:
            target.msg("Ты самовыпилился.")
            caller.location.msg_contents("%s самовыпилился." % (caller.key),exclude=caller)

        target.at_die()

        weapon.db.durability = weapon.db.durability - 1
        caller.msg("Твое оружие утратило одно очко запаса прочности. {wЗапас просности: %s{n" % weapon.db.durability)

        if weapon.db.durability > 0:
            return

        okey = weapon.delete()

        if not okey:
            caller.msg("Не удалось уничтожить оружие.")
        else:
            caller.msg("Твою оружие сломалось и рассыпалось в пыль.")
            return

class CmdAlchemy(Command):
    """
    Команда для изъятия объектов их рук
    """
    key = "alchemy"
    aliases = [u"алхимия"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller

        if not self.args:
            caller.msg("Использование (без <>): алхимия <ингредиент 1>+<ингредиент 2>+<ингредиент 3>+...")
            return

        componets = self.args.strip().split("+")

        if not componets:
            caller.msg("Не верно указаны ингредиенты.")
            return
        
        avaible_components,to_delete = [],[]
        for componet in componets:
            avaible = caller.search(componet, location=caller, nofound_string="У тебя нет компонента: %s" % componet)
            if not avaible:
                continue
            avaible_components.append(avaible.key)
            to_delete.append(avaible)

        if len(componets) != len(avaible_components):
            caller.msg("У тебя не хватает компонентов!")
            return
        
        recipes = Alchemy().recipes.values()
        created= False

        for recipe in recipes:
            if self.comp(list1=avaible_components, list2=recipe["components"]):
                result = create_object(recipe["typeclass"], recipe["name"], caller, home=caller)
                created = True

        if not created:
            caller.msg("Нет такого рецепта!")
            return

        string = "Ты потратил: "
        for item in to_delete:
            string += "%s, " % item.key
            item.delete()
        string+="и нахимичил %s" % result.key
        caller.msg(string)


    def comp(self, list1, list2):
        for val in list1:
            if val in list2:
                return True
        return False
                        
class CmdFollow(Command):
    """
    нужна что вступать в пати
    """
    key = u"follow"
    aliases = [u"следовать"]
    locks = "cmd:all()"
    help_category = "General"
    
    def yesno(self, caller, prompt, result): 
        if result.lower() in ("д", "да", "н", "нет"):
            
            if result.lower() in ("да","д"):

                caller.db.party.append(self.caller.key)
                self.caller.db.party_leader = caller.key
                self.caller.msg("Тебя добавили в группу.")
                caller.msg("Ты добавил %s в группу" % self.caller.key)
            
            if result.lower() in ("нет","н"):
                
                self.caller.msg("Тебе отказали.")
        else:
            # the answer is not on the right yes/no form
            caller.msg("Ответьте 'да' или 'нет'. \n%s" % prompt)
            # returning True will make sure the prompt state is not exited
            return True

    def func(self):
        caller = self.caller

        args = self.args.strip()

        leader = caller.db.party_leader

        if not args:
            if not leader:
                caller.msg("Ты и так не состоишь в группе.")
                return
        
            leader_search = caller.search(leader, global_search=True,nofound_string="Такого лидера нет.")
        
            if not leader_search:
                return

            leader_search.db.party.remove(caller.key)
            caller.db.party_leader = None
            caller.msg("Ты вышел из группы лидера %s." % leader_search.key)
            leader_search.msg("Из твой группы вышел %s" % caller.key)
            return

        leader_to_follow = caller.search(args, location=caller.location, global_search=True,nofound_string="Такого игрока нет.")

        if not leader_to_follow:
            return

        if not leader_to_follow.has_player:
            caller.msg("Игрок %s не в сети. Ты пока не можешь присоединиться к нему." % leader_to_follow.key)
            return
        
        get_input(leader_to_follow, "Игрок %s хочет к вам присоединиться, ты согласен? (Да/Нет)" % caller.key, self.yesno)
        caller.msg("Ты подал запрос на вступление в группу. Жди пока %s ответит." % leader_to_follow.key)


class CmdKikcFromParty(Command):
    """
    Нужна чтобы турнуть из пати
    """
    key = u"kick"
    aliases = [u"дропнуть", u"турнуть", u"выгнать", u"кикнуть"]
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
    
        caller = self.caller

        args = self.args.strip()

        if not args:
            caller.msg("Кого выгнать из группы?")
            return

        if not caller.db.party:
            caller.msg("Ты не лидер группы, ты не можешь никого выгнать.")
            return

        if args in caller.db.party:
            caller.db.party.remove(args)
            caller.msg("Ты выгнал %s из группы." % args)
        
        player = caller.search(args, global_search=True,nofound_string="Такого игрока нет.")

        if not player:
            return

        player.msg("Тебя выгнали из группы.")
        player.db.party_leader = None


class CmdReligionChange(Command):
    """
    Нужна чтобы уверовать в разных богов
    """
    key = u"religion"
    aliases = [u"религия", u"уверовать"]
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
    
        caller = self.caller

        args = self.args.strip()

        if not args:
            string = " "
            for rel in caller.avaible_religions:
                string += "%s, " % rel
            caller.msg("Какую религию выберешь? Доступны: %s" % string)
            return

        if args == "отречься":
            caller.msg("Ты стал атеистом")
            caller.location.msg_contents("%s разочаровался в своих богах и отрекся от них. Теперь он атеист." % (caller.key),exclude=caller)
            caller.db.religion = "атеист"
            return
 
        if not args.lower() in caller.avaible_religions:
            caller.msg("Такой религии нет в этом мире.")
            return

        if caller.db.religion:
            caller.msg("Ты сменил религию с %s на %s" % (caller.db.religion, args))
            caller.location.msg_contents("%s сменил религию на %s" % (caller.key, args),exclude=caller)
            caller.db.religion = args
        else:
            caller.msg("Ты уверовал в %s" % args)
            caller.location.msg_contents("%s подался в %s" % (caller.key, args),exclude=caller)
            caller.db.religion = args

class CmdBack(Command):
    """
    Нужна чтобы уверовать в разных богов
    """
    key = u"back"
    aliases = u"назад"
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
    
        caller = self.caller

        args = self.args.strip()

        if not caller.db.last_location:
            caller.msg("Ты не можешь вернуться в предыдущую локацию.")
            return

        last_location = caller.db.last_location
        
        if caller.location == last_location:
            caller.msg("Ты уже в предыдущей локации.")
            return
        
        caller.move_to(last_location,quiet=True)
        caller.msg("Ты вернулся в предыдущую локацию.")
