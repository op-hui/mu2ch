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

Sup, Анонимус! 
Добро пожаловать на тестовый сервер MUDча.

Что бы войти на сервер введите:
        {wвойти <username> <password> {n
Что бы создать аккаунт введите:
        {wсоздать <username> <password> {n

Инструкция для новичков:

В каждой локации есть выходы - локации в которые можно перейти из вашей текущей. Для перемещения в нужную вам локацию наберите в строке ввода её название.
Например: "восток", "юг", "Сычевальня". Названия регистронезависимые.

Для общения с другими игроками или NPC используйте команду «say текст» или «сказать текст». Например:
'сказать Пролетарии всех стран соединяйтесь!'
Если вы хотите поговорить с NPC, то после команды сказать введите имя NPC. Например:
'сказать Леночка'

Что бы получить дополнительную информацию используйте команду «help».

Более подробно:
Инструкция по взаимодействию с игровым миром и передвижению по его локациям:
        https://github.com/op-hui/mu2ch/blob/master/guide/faq.md
        
Для разработчиков и просто желающих помочь:
Основная страница разработчиков на GitHub:
        https://github.com/op-hui/mu2ch
Конференция в Jabber:
        mu2ch@conference.jabber.ru

{b=============================================================={n"""

#CONNECTION_SCREEN = \
#"""{b=============================================================={n
# Сап анон! Тестовый сервер Мудача приветствует тебя
#
# Если у тебя есть аккаунт, набери
#      {wconnect <username> <password>{n
# Если аккаунта нет, то создай:
#      {wcreate <username> <password>{n
#
# Основная страница:
#    https://github.com/op-hui/mu2ch
#
# Гайды как пилить свои локации, объекты, мобов, даже небо, даже аллаха:
#    https://github.com/op-hui/mu2ch/wiki
#    
#
# F.A.Q: как передвигаться между локациями, ходить, фапать, телебонить
#    https://github.com/op-hui/mu2ch/blob/master/guide/faq.md
#
# Конференция в жаббере:
#    mu2ch@conference.jabber.ru
#
# Краткий гайд:
#    1. В каждой локации есть выходы, что бы выйти в нужном направлении,
#набери имя выхода
#    2. Говорить - команда сказать или ", например "sup
#    3. Лоли в коридоре отдается на шоколадные конфеты
#    
# Если команда help
#{b=============================================================={n""" 
# 
