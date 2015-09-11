# -*- coding: utf-8 -*-
"""
Connection screen

Texts in this module will be shown to the user at login-time.

Evennia will look at global string variables (variables defined
at the "outermost" scope of this module and use it as the
connection screen. If there are more than one, Evennia will
randomize which one it displays.

The commands available to the user when the connection screen is shown
are defined in commands.default_cmdsets.UnloggedinCmdSet and the
screen is read and displayed by the unlogged-in "look" command.

"""

from django.conf import settings
from evennia import utils

CONNECTION_SCREEN = \
"""{b=============================================================={n
 Сап анон! Тестовый сервер Мудача приветствует тебя

 Если у тебя есть аккаунт, набери
      {wconnect <username> <password>{n
 Если аккаунта нет, то создай:
      {wcreate <username> <password>{n

 Основная страница:
    https://github.com/op-hui/mu2ch

 Гайды как пилить свои локации, объекты, мобов, даже небо, даже аллаха:
    https://github.com/op-hui/mu2ch/wiki
    

 F.A.Q: как передвигаться между локациями, ходить, фапать, телебонить
    https://github.com/op-hui/mu2ch/blob/master/guide/faq.md

 Конференция в жаббере:
    mu2ch@conference.jabber.ru

 Краткий гайд:
    1. В каждой локации есть выходы, что бы выйти в нужном направлении,
набери имя выхода
    2. Говорить - команда сказать или ", например "sup
    3. Лоли в коридоре отдается на шоколадные конфеты
    
 Если команда help
{b=============================================================={n""" 
 
