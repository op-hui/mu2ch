ЧТО ДЕЛАЮТ БИЛДЕРЫ: 
Вводная:
  * @create Пека - создать предмет в инвентаре
  * inv - инвентарь
  * drop Пека - бросить предмет  
  * get Пека - взять пеку
  * @create/drop Хуй - создать и бросить хуй 
  * @desc ХУЙ ОП задать описание локации или предмета
  * @dig (название локации) = (название входа в локацию из текущей комнаты) - 
  * создать комнату с входом из текущей локации
  * @open (название выхода из локации) = (локация, в которую ведет выход) - создает выход из текущей локации в указанную локацию

Внятная дока для продолжения:
https://github.com/evennia/evennia/wiki/Building%20Quickstart

Еще гайд:

Гойд фор ту комманд @dig. @dig- создает трэп хату бабусю и гусей с выходом                                                                                         (фор buillder)

@open [напрвление(north, east, south, west)]; [алиас входа] = [имя комнаты] - создаст в комнате выход в указанном направлении с указанным названием направления и указнным алиасом.

@open [название выхода] = [название локации] - создает выход с указанным названием из текущей локации в указанную локацию.

@dig((/teleport)типа ебать создаешь и сразу туда телепортируешся) тута имя типа ёпты бля = (нужен для разделения имени и выхода) тута нахуй выход ебать;(для разделения) ищо выход; ищо один

Гойд фор ту комманд @create. @create- создает предмет ебать (придметы, созданные @create в инвентаре (@inventory))

@create((/drop) эта кароч как создал дилдос и сразу выкинул из инвентаря ебать. Ахуенная вещ.) тута имя йопту                                      (фор buillder)

Гойд ту команд drop. drop- бросить предмет, дилдос, мою бабку. (зомете, что эта комманда без @, все правильна).

drop и вот тута нада написать придмет, ты его выбросишь.

Гойд фор ту комманд @desc [имя предмета] = [текст описания] - задет описание игроку, предмету, твоей мамке. Описание показывается когда делаешь look.

Гойд фор ту комманд @name [имя предмета] = [новое имя];[алиас];[алиас];... - переименовывает предмет и при указание алиасов зажает алиасы.

Гойд фор ту комманд @set [имя предемета]/[атрибут предмета] = значение атрибута -создает атрибут объекту или редактирует уже имеющийся, пока не знаю зачем это нужно но вешь думаю полезная.для скриптов(хуиптов(охуенная шутка за триста)),но она и в командной строке работает

потом еще нужно будет написать по @spawn {ключь:значение, ключ:значение,...}

Гойд фор ту команд look. look- это осмотрется, осмотреть дилдос.

(зомете что при обычном look, тоес look без ничего, вы увидите, что около вас, в комннате, на трэп хате, около параши придметы и/или игрок. Но еси вы напишите, например, look дилдос, то вы посмотрете уже на придмет + ето работает еще и с игроком, например: look и тут какойта хуисос  но мне кажется это тоже самое что и простое look).

look %дилдоснаем%

Гойд фор ту команд home. home- возвращает тебя, твою бабусю или в лимб(начало всея руси) либа домой, на треп хату.

home

Гойд фор ту команд @teleport. @teleport- эта кароч или телепортироваться/телепортировать себя/предмет/свою бабусю/игрока, к игроку/в треп хату/ к самому себе.

@teleport(/switches

Гойд фор ту команд @alias. @alias[имя объекта] = [алиас];[алиас];...-  это такое гавно боже нахуй ебать. Кароч оно делать так чоб вместа look  была осмотрется ебать. Или это дополнительные имена объектов йобана.

поясняю за алиасы- это дополнительные имена объектов. если есть объект "дилдо" и у него есть алиасы "вибратор, резиновый член" - то при вызове "look вибратор" мы получим описание и основное имя дилдо. типа того. или еще можно назвать их ссылками на объект.

