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
        self.db.desc = u"""Нечто вечно всем недовольное, лежащее на продавленном диване в дырявых трениках с отвисшей мотнёй. 
В руках бульварная газета и пульт от телевизора с транслируемым политическим ток-шоу. 
Отцеподобное существо любит царственно почёсывать пивное брюхо, обожает пятничный преферанс и вяленую воблу, 
готово до хрипоты в горле спорить о преимуществе блесны над мормышкой и макушатника над дождевыми червями. 
Профессор кроссвордогадания летом выходит играть в домино прямо в домашних тапочках, бритьё подмышек и дезодоранты считает уделом педерастов. 
Сортирный генерал категорически отказывается пользоваться обувной ложкой и ситечком для чая. 
Жлобатько не пьёт шмурдяк в баре биллиардного клуба, а заранее накачивается рядом в киоске-наливайке, где гранчак аналогичной бурды на рубль дешевле. 
Диванный князёк кроет жену нецензурной бранью за невымытую тарелку и слабо нагретый ужин, 
хотя сам не менял носки три недели и мылся «когда последний раз горячая вода в кране была». На бойлер денег скопить надо, экономить на пойле придётся, устанавливать его потом — гембель, сопоставимый по объёмам со строительством БАМа.
"""

        self.cmdset.add(CmdSetTest)
        self.locks.add("call:false()")
        self.locks.add("get:false()")

    def at_object_receive(self, obj, source_location):
        if obj.key == "травы":
          self.execute_cmd("say Ой, мне нужно в туалет")
        else:
          self.execute_cmd("say Путин - лучший президент!")
