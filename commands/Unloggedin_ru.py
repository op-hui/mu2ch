# -*- coding: utf-8 -*-
"""
Команды для логина и создания пользователя
"""
import re
import traceback
import time
from collections import defaultdict
from random import getrandbits
from django.conf import settings
from evennia.players.models import PlayerDB
from evennia.objects.models import ObjectDB
from evennia.server.models import ServerConfig
from evennia.comms.models import ChannelDB
from evennia.commands.default.unloggedin import _create_player, _create_character
from evennia.utils import create, logger, utils, ansi
from evennia.commands.default.muxcommand import MuxCommand
from evennia.commands.cmdhandler import CMD_LOGINSTART


MULTISESSION_MODE = settings.MULTISESSION_MODE

MULTISESSION_MODE = settings.MULTISESSION_MODE
CONNECTION_SCREEN_MODULE = settings.CONNECTION_SCREEN_MODULE

# Helper function to throttle failed connection attempts.
# This can easily be used to limit player creation too,
# (just supply a different storage dictionary), but this
# would also block dummyrunner, so it's not added as default.

_LATEST_FAILED_LOGINS = defaultdict(list)
def _throttle(session, maxlim=None, timeout=None,
                   storage=_LATEST_FAILED_LOGINS):
    """
    This will check the session's address against the
    _LATEST_LOGINS dictionary to check they haven't
    spammed too many fails recently.

    Args:
        session (Session): Session failing
        maxlim (int): max number of attempts to allow
        timeout (int): number of timeout seconds after
            max number of tries has been reached.

    Returns:
        throttles (bool): True if throttling is active,
            False otherwise.

    Notes:
        If maxlim and/or timeout are set, the function will
        just do the comparison, not append a new datapoint.

    """
    address = session.address
    if isinstance(address, tuple):
        address = address[0]
    now = time.time()
    if maxlim and timeout:
        # checking mode
        latest_fails = storage[address]
        if latest_fails and len(latest_fails) >= maxlim:
            # too many fails recently
            if now - latest_fails[-1] < timeout:
                # too soon - timeout in play
                return True
            else:
                # timeout has passed. Reset faillist
                storage[address] = []
                return False
    else:
        # store the time of the latest fail
        storage[address].append(time.time())
        return False


class CmdUnconnectedConnectRu(MuxCommand):
    """
    connect to the game

    Usage (at login screen):
      connect playername password
      connect "player name" "pass word"

    Use the create command to first create an account before logging in.

    If you have spaces in your name, enclose it in quotes.
    """
    key = u"connect"
    aliases = [u"conn", u"con", u"co",u"подкл",u"коннект",u"кон",u"ко",u"войти"]
    locks = "cmd:all()"  # not really needed
    arg_regex = r"\s.*?|$"

    def func(self):
        """
        Uses the Django admin api. Note that unlogged-in commands
        have a unique position in that their func() receives
        a session object instead of a source_object like all
        other types of logged-in commands (this is because
        there is no object yet before the player has logged in)
        """
        session = self.caller

        # check for too many login errors too quick.
        if _throttle(session, maxlim=5, timeout=5*60, storage=_LATEST_FAILED_LOGINS):
            # timeout is 5 minutes.
            session.msg("{RВы совершаете слишклм много подключений. Подождите пару минут и попробуйте снова.{n")
            return

        args = self.args
        # extract quoted parts
        parts = [part.strip() for part in re.split(r"\"|\'", args) if part.strip()]
        if len(parts) == 1:
            # this was (hopefully) due to no quotes being found, or a guest login
            parts = parts[0].split(None, 1)
            # Guest login
            if len(parts) == 1 and parts[0].lower() == "guest" and settings.GUEST_ENABLED:
                try:
                    # Find an available guest name.
                    for playername in settings.GUEST_LIST:
                        if not PlayerDB.objects.filter(username__iexact=playername):
                            break
                        playername = None
                    if playername == None:
                        session.msg("Все гостевые аккаунты сейчас используются. Попробуйте немного позже.")
                        return

                    password = "%016x" % getrandbits(64)
                    home = ObjectDB.objects.get_id(settings.GUEST_HOME)
                    permissions = settings.PERMISSION_GUEST_DEFAULT
                    typeclass = settings.BASE_CHARACTER_TYPECLASS
                    ptypeclass = settings.BASE_GUEST_TYPECLASS
                    new_player = _create_player(session, playername, password,
                                                permissions, ptypeclass)
                    if new_player:
                        _create_character(session, new_player, typeclass,
                                        home, permissions)
                        session.sessionhandler.login(session, new_player)

                except Exception:
                    # We are in the middle between logged in and -not, so we have
                    # to handle tracebacks ourselves at this point. If we don't,
                    # we won't see any errors at all.
                    string = "%s\nЭто баг. Напишите пожалуйста на почту администратора."
                    session.msg(string % (traceback.format_exc()))
                    logger.log_errmsg(traceback.format_exc())
                finally:
                    return

        if len(parts) != 2:
            session.msg("\n\r Использование (без <>): коннект <имя пользователя> <пароль>. Сокашенные варианты: кон, ко, войти")
            return
        playername, password = parts

        # Match account name and check password
        player = PlayerDB.objects.get_player_from_name(playername)
        pswd = None
        if player:
            pswd = player.check_password(password)

        if not (player and pswd):
            # No playername or password match
            string = "Неверные логин или пароль.\nЕсли в вашем логине или " \
                     "пароле есть пробелы, поместите их в кавычки." \
                     "\nЕсли вы новичек, создайте аккаунт при помощи" \
                     "команды 'создать'."
            session.msg(string)
            # this just updates the throttle
            _throttle(session, storage=_LATEST_FAILED_LOGINS)
            # calls player hook for a failed login if possible.
            if player:
                player.at_failed_login(session)
            return

        # Check IP and/or name bans
        bans = ServerConfig.objects.conf("server_bans")
        if bans and (any(tup[0]==player.name.lower() for tup in bans)
                     or
                     any(tup[2].match(session.address) for tup in bans if tup[2])):
            # this is a banned IP or name!
            string = "{rВы были забанены." \
                     "\nЕсли считате, что мы были не правы, пишите на е-маил администратора.{x"
            session.msg(string)
            session.execute_cmd("quit")
            return

        # actually do the login. This will call all other hooks:
        #   session.at_login()
        #   player.at_init()  # always called when object is loaded from disk
        #   player.at_pre_login()
        #   player.at_first_login()  # only once
        #   player.at_post_login(sessid=sessid)
        session.sessionhandler.login(session, player)


class CmdUnconnectedCreateRu(MuxCommand):
    """
    create a new player account

    Usage (at login screen):
      create <playername> <password>
      create "player name" "pass word"

    This creates a new player account.

    If you have spaces in your name, enclose it in quotes.
    """
    key = u"create"
    aliases = [u"cre", u"cr", u"создать"]
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
        if not re.findall('^[\w. @+-]+$', playername,re.UNICODE) or not (0 < len(playername) <= 30):
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
        if not re.findall('^[\w. @+-]+$', password,re.UNICODE) or not (3 < len(password)):
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

class CmdSetHelp_RU(MuxCommand):
    """
    edit the help database

    Usage:
      @help[/switches] <topic>[,category[,locks]] = <text>

    Switches:
      add    - add or replace a new topic with text.
      append - add text to the end of topic with a newline between.
      merge  - As append, but don't add a newline between the old
               text and the appended text.
      delete - remove help topic.
      force  - (used with add) create help topic also if the topic
               already exists.

    Examples:
      @sethelp/add throw = This throws something at ...
      @sethelp/append pickpocketing,Thievery = This steals ...
      @sethelp/append pickpocketing, ,attr(is_thief) = This steals ...

    This command manipulates the help database. A help entry can be created,
    appended/merged to and deleted. If you don't assign a category, the
    "General" category will be used. If no lockstring is specified, default
    is to let everyone read the help file.

    """
    key = "@help"
    aliases = ["@sethelp","@помощь"]
    locks = "cmd:perm(PlayerHelpers)"
    help_category = "Building"

    def func(self):
        "Implement the function"

        switches = self.switches
        lhslist = self.lhslist

        if not self.args:
            self.msg("Использование: @sethelp/[add|del|append|merge] <заголвок>[,категория[,ограничения,..] = <текст>")
            return

        topicstr = ""
        category = "General"
        lockstring = "view:all()"
        try:
            topicstr = lhslist[0]
            category = lhslist[1]
            lockstring = ",".join(lhslist[2:])
        except Exception:
            pass

        if not topicstr:
            self.msg("Ты должен определить тему!")
            return
        # check if we have an old entry with the same name
        try:
            old_entry = HelpEntry.objects.get(db_key__iexact=topicstr)
        except Exception:
            old_entry = None

        if 'append' in switches or "merge" in switches:
            # merge/append operations
            if not old_entry:
                self.msg("Не могу найти тему '%s'. Ты должен дать точное название." % topicstr)
                return
            if not self.rhs:
                self.msg("Ты должен указать текст append/merge.")
                return
            if 'merge' in switches:
                old_entry.entrytext += " " + self.rhs
            else:
                old_entry.entrytext += "\n%s" % self.rhs
            self.msg("Всутпление обновлено:\n%s" % old_entry.entrytext)
            return
        if 'delete' in switches or 'del' in switches:
            # delete the help entry
            if not old_entry:
                self.msg("Не могу найти тему '%s'" % topicstr)
                return
            old_entry.delete()
            self.msg("Удалено '%s'." % topicstr)
            return

        # at this point it means we want to add a new help entry.
        if not self.rhs:
            self.msg("Ты должен указать текст.")
            return
        if old_entry:
            if 'for' in switches or 'force' in switches:
                # overwrite old entry
                old_entry.key = topicstr
                old_entry.entrytext = self.rhs
                old_entry.help_category = category
                old_entry.locks.clear()
                old_entry.locks.add(lockstring)
                old_entry.save()
                self.msg("Переписана тема '%s' на новую." % topicstr)
            else:
                self.msg("Топик '%s' уже существует. Используй /force для перезаписи или /append или /merge чтобы добавить текст." % topicstr)
        else:
            # no old entry. Create a new one.
            new_entry = create.create_help_entry(topicstr,
                                                 self.rhs, category, lockstring)
            if new_entry:
                self.msg("Топик '%s' был успешно создан." % topicstr)
            else:
                self.msg("Ошибка при создании темы '%s'! Свяжитесь с админом." % topicstr)

class CmdUnconnectedHelp_ru(MuxCommand):
    """
    get help when in unconnected-in state

    Usage:
      help

    This is an unconnected version of the help command,
    for simplicity. It shows a pane of info.
    """
    key = "help"
    aliases = ["h", "?","помощь"]
    locks = "cmd:all()"

    def func(self):
        "Shows help"

        string = \
            """
ТЫ еще не вошел в игру. Здесь тебе доступны команды:

  {wcreate{n - создать аккаунт
  {wconnect{n - войти по уже существующему
  {wlook{n - перезагруть приветственный экран
  {whelp{n - показать эту помощь
  {wencoding{n - указать кодировку подходящую вашему коленту
  {wscreenreader{n - подстроить экран
  {wquit{n - выйти

Сначала создай аккаунт при помощи {wcreate [ИМЯ] [ТВОЙ ЕБУЧИЙ ПАРОЛЬ]
(Если захотел имя из нескольких слов - используй кавычки: {wcreate "[ТВОЕ ИМЯ ИЗ НЕСКОЛЬКИХ СЛОВ]" [ТВОЙ ЕБУЧИЙ ПАРОЛЬ]
Потом, как создал все гавно, подключайся: {wconnect [ИМЯ] [ТВОЙ ЕБУЧИЙ ПАРОЛЬ]

Напиши {wlook{n command если хочешь посмотреть приветсвие нашего сервера еще раз.

"""
        self.caller.msg(string)
