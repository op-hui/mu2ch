# -*- coding: utf-8 -*-
"""
The help command. The basic idea is that help texts for commands
are best written by those that write the commands - the admins. So
command-help is all auto-loaded and searched from the current command
set. The normal, database-tied help system is used for collaborative
creation of other help topics such as RP help or game-world aides.
"""

from django.conf import settings
from collections import defaultdict
from evennia.utils.utils import fill, dedent
from evennia.commands.command import Command
from evennia.help.models import HelpEntry
from evennia.utils import create
from evennia.utils.utils import string_suggestions
from evennia.commands.default.muxcommand import MuxCommand

# limit symbol import for API
__all__ = ("CmdHelp", "CmdSetHelp")
_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH
_SEP = "{C" + "-" * _DEFAULT_WIDTH + "{n"


def format_help_entry(title, help_text, aliases=None, suggested=None):
    """
    This visually formats the help entry.
    """
    string = _SEP + "\n"
    if title:
        string += "{CПомощь по {w%s{n" % title
    if aliases:
        string += " {C(еще варианты: %s{C){n" % ("{C,{n ".join("{w%s{n" % ali for ali in aliases))
    if help_text:
        string += "\n%s" % dedent(help_text.rstrip())
    if suggested:
        string += "\n\n{CПредложено:{n "
        string += "%s" % fill("{C,{n ".join("{w%s{n" % sug for sug in suggested))
    string.strip()
    string += "\n" + _SEP
    return string


def format_help_list(hdict_cmds, hdict_db):
    """
    Output a category-ordered list. The input are the
    pre-loaded help files for commands and database-helpfiles
    resectively.
    """
    string = ""
    if hdict_cmds and any(hdict_cmds.values()):
        string += "\n" + _SEP + "\n   {CПомощь по командам{n\n" + _SEP
        for category in sorted(hdict_cmds.keys()):
            string += "\n  {w%s{n:\n" % (str(category).title())
            string += "{G" + fill(", ".join(sorted(hdict_cmds[category]))) + "{n"
    if hdict_db and any(hdict_db.values()):
        string += "\n\n" + _SEP + "\n\r  {CДругая помощь{n\n" + _SEP
        for category in sorted(hdict_db.keys()):
            string += "\n\r  {w%s{n:\n" % (str(category).title())
            string += "{G" + fill(", ".join(sorted([str(topic) for topic in hdict_db[category]]))) + "{n"
    return string


class CmdHelp_ru(Command):
    """
    view help or a list of topics

    Usage:
      help <topic or command>
      help list
      help all

    This will search for help on commands and other
    topics related to the game.
    """
    key = "help"
    aliases = "помощь"
    locks = "cmd:all()"

    # this is a special cmdhandler flag that makes the cmdhandler also pack
    # the current cmdset with the call to self.func().
    return_cmdset = True

    def parse(self):
        """
        input is a string containing the command or topic to match.
        """
        self.original_args = self.args.strip()
        self.args = self.args.strip().lower()

    def func(self):
        """
        Run the dynamic help entry creator.
        """
        query, cmdset = self.args, self.cmdset
        caller = self.caller

        suggestion_cutoff = 0.6
        suggestion_maxnum = 5

        if not query:
            query = "all"

        # removing doublets in cmdset, caused by cmdhandler
        # having to allow doublet commands to manage exits etc.
        cmdset.make_unique(caller)

        # retrieve all available commands and database topics
        all_cmds = [cmd for cmd in cmdset if cmd.auto_help and cmd.access(caller)]
        all_topics = [topic for topic in HelpEntry.objects.all() if topic.access(caller, 'view', default=True)]
        all_categories = list(set([cmd.help_category.lower() for cmd in all_cmds] + [topic.help_category.lower() for topic in all_topics]))

        if query in ("list", "all"):
            # we want to list all available help entries, grouped by category
            hdict_cmd = defaultdict(list)
            #hdict_cmd_ali = defaultdict(list)
            hdict_topic = defaultdict(list)
            # create the dictionaries {category:[topic, topic ...]} required by format_help_list
            [hdict_cmd[cmd.help_category].append(cmd.key) for cmd in all_cmds]
            [hdict_cmd[cmd.help_category].extend(cmd.aliases) for cmd in all_cmds]
            [hdict_topic[topic.help_category].append(topic.key) for topic in all_topics]
            # report back
            self.msg(format_help_list(hdict_cmd, hdict_topic))
            return

        # Try to access a particular command

        # build vocabulary of suggestions and rate them by string similarity.
        vocabulary = [cmd.key for cmd in all_cmds if cmd] + [topic.key for topic in all_topics] + all_categories
        [vocabulary.extend(cmd.aliases) for cmd in all_cmds]
        suggestions = [sugg for sugg in string_suggestions(query, set(vocabulary), cutoff=suggestion_cutoff, maxnum=suggestion_maxnum)
                       if sugg != query]
        if not suggestions:
            suggestions = [sugg for sugg in vocabulary if sugg != query and sugg.startswith(query)]

        # try an exact command auto-help match
        match = [cmd for cmd in all_cmds if cmd == query]
        if len(match) == 1:
            self.msg(format_help_entry(match[0].key,
                     match[0].__doc__,
                     aliases=match[0].aliases,
                     suggested=suggestions))
            return

        # try an exact database help entry match
        match = list(HelpEntry.objects.find_topicmatch(query, exact=True))
        if len(match) == 1:
            self.msg(format_help_entry(match[0].key,
                     match[0].entrytext,
                     suggested=suggestions))
            return

        # try to see if a category name was entered
        if query in all_categories:
            self.msg(format_help_list({query:[cmd.key for cmd in all_cmds if cmd.help_category==query]},
                                        {query:[topic.key for topic in all_topics if topic.help_category==query]}))
            return

        # no exact matches found. Just give suggestions.
        self.msg(format_help_entry("", "Не найдена помощь по '%s'" % query, None, suggested=suggestions))
