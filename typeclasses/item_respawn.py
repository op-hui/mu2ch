# -*- coding: utf-8 -*-
""" обработчик респауна объектов """

from evennia import DefaultScript
from typeclasses.objects import Object
from typeclasses.weapons import AcidBottle, Knife, Pistol
from django.conf import settings
from evennia import create_object, search_object
import random

class RespawnHandler(DefaultScript):
	"""обработчик респауна объектов
	   typeclass - класс объекта
	   name - имя объекта
	   locations - список локаций где будут размещены предметы
	   desc - описание объекта, если оне не задано при создании
	   world_count - количество таких объектов в мире
	"""
	#словарь с инсрукциями: что создавть, где создать, сколько этого должно быть
	instruction = {"1" : {"typeclass" : settings.BASE_OBJECT_TYPECLASS, "name": "Дилдо твоей мамки", "locations":["1-test","1-test2"], "desc": "Кто-то выкинул во двор дилдо товоей мамки.", "world_count": 2},
			   	   "2" : {"typeclass" : Knife, "name": "Картонный нож", "locations":["test3"], "desc": None, "world_count": 1}
			  	  }


	def at_script_creation(self):
		#имя скрипта
		self.key = "spawn_script"
		#описание
		self.desc = "Спаунит вещи в локациях каждую минуту."
		#интервал с которым выполняется метод at_repeat
		self.interval = 30 
		#Переживет ли скрипт перезагрузку сервера. Типа авто запуска скрипта.
		self.persistent = True

	def at_repeat(self):
		if not self.instruction:
			return

		inst_list = self.instruction.values()

		if not inst_list:
			return

		for inst in inst_list:
			#ищем текущий предмет
			items = search_object(inst["name"])

			#если нет таких передметов
			if not items:
				#self.obj.msg_contents("не нашел %s" % inst["name"])
				for count in range(inst["world_count"]):
					self.obj.msg_contents("создаю %s" % inst["name"])
					#берем рандомную локацию из списка локаций
					location = random.choice(inst["locations"])
					self.obj.msg_contents("выбрал %s" % location)
					#ищем ее
					loc = search_object(location)
					self.obj.msg_contents("нашел %s" % loc)
					#если их много как кухонь то, из них берем рандомную
					creation_loc = random.choice(loc)
					self.obj.msg_contents("выбрал %s" % creation_loc.key)
					#создаем там объект
					obj = create_object(inst["typeclass"],inst["name"], creation_loc)
					self.obj.msg_contents("создал %s" % obj.key)
					# буду к этому вязяться когда будут предметы с одинаоквыми именами
					obj.db.respawnable = True
					#задаем описание если нет стандартного как у ножа	
					if inst["desc"]:
						if not obj.db.desc:
							obj.db.desc = inst["desc"]

			#если предметы найдены				
			else:
				#self.obj.msg_contents("нашел %s" % items)
				#если их меньше чем задано в world_count
				if len(items) < inst["world_count"]:
					self.obj.msg_contents("добвляю не достоющие %s" % inst["name"])
					#создаем не достающее количество объектов
					for count in range(inst["world_count"] - len(items)):
						#берем рандомнуб локацию из списка локаций
						location = random.choice(inst["locations"])
						self.obj.msg_contents("выбрал %s" % location)
						#ищем ее
						loc = search_object(location)
						self.obj.msg_contents("нашел %s" % loc)
						#если их много как кухонь то, из них берем рандомную
						creation_loc = random.choice(loc)
						self.obj.msg_contents("выбрал %s" % creation_loc.key)
						#создаем там объект
						obj = create_object(inst["typeclass"],inst["name"], creation_loc)
						self.obj.msg_contents("создал %s" % obj.key)
						# буду к этому вязяться когда будут предметы с одинаоквыми именами
						obj.db.respawnable = True
						#задаем описание если нет стандартного как у ножа	
						if inst["desc"]:
							if not obj.db.desc:
								obj.db.desc = inst["desc"]

