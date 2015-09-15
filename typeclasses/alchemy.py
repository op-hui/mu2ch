# -*- coding: utf-8 -*-
"""
класс для алхимических рецептов и компонентов
"""
from typeclasses.objects import Object
from typeclasses.weapons import AcidBottle
from django.conf import settings

class Alchemy(object):

	recipes = {"1" : {"typeclass" : AcidBottle, "name": "бутылка с кислотой", "components":["сера","водород","бутылка"]},
			   "2" : {"typeclass" : settings.BASE_OBJECT_TYPECLASS, "name": "Бэйлис", "components":["кофе 3в1","водка"]}
			  }


