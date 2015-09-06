# -*- coding: utf-8 -*-
from evennia import DefaultObject, CmdSet
from evennia import default_cmds

class CmdSetTest(CmdSet):
     def at_cmdset_creation(self):
         self.add(default_cmds.CmdSay())

class YourMom(DefaultObject):
    def at_object_creation(self):
        self.cmdset.add(CmdSetTest)
        self.locks.add("call:false()")
    def at_object_receive(self, obj, source_location):
        self.execute_cmd("say Хороший сына растет, спасибо за %s, %s!" % (obj, source_location))

class YourDad(DefaultObject):
    def at_object_creation(self):
        self.cmdset.add(CmdSetTest)
        self.locks.add("call:false()")

    def at_object_receive(self, obj, source_location):
        if obj.key == "травы":
          self.execute_cmd("say Ой, мне нужно в туалет")
        else:
          self.execute_cmd("say Путин - лучший президент!")
