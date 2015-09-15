# -*- coding: utf-8 -*-
"""
класс для алхимических рецептов и компонентов
"""
from typeclasses.objects import Object
from typeclasses.weapons import AcidBottle

class Alchemy(object):

	recipes = {["сера","водород","бутылка"] : {"typeclass" : AcidBottle, "name": "бутылка с кислотой"}}


