# -*- coding: utf-8 -*-
from evennia import DefaultObject, CmdSet
from evennia import default_cmds
import random
from evennia import syscmdkeys
from commands.command import CmdTalk
from evennia import Command, CmdSet, utils
from evennia.contrib import menusystem
from typeclasses.objects import Object
from evennia import create_object
from django.conf import settings

class CmdSetTest(CmdSet):
     def at_cmdset_creation(self):
         self.add(default_cmds.CmdSay())
         

def simpleNPC(Object):
    def at_object_creation(self):
        self.db.npc = True
        self.locks.add("call:false()")
        self.locks.add("get:false()")
    

class YourMom(Object):
    descriptions = [
            u"""селянка, но поинтеллегентнее, дворянского рода. Закончила школу и молочный техникум. Овуляха по жизнипо интересам. Дети на первом месте, что полезно, ибо помогает всегда деньгами. Изменяет отцу с кем ни попадя. Поженились, похоже, по залету. Один раз изменяла в соседней комнате, когда мне было около пяти лет, а я и тогда все понимал. Наверное, это как-то повлияло на то, что своим девушкам я не доверяю и даже в сексе расслабиться и кончить не могу.""",
            u"""закончила 8 классов и быдлошарагу. Курит, по её словам, с 16 лет. По профессии не работала, смыслом жизни считает выращивание детей, во всех своих бедах винит тоже их. Родила моего брата в 20 лет. Во сколько вышла замуж я хз, но там был какой-то скандал, их родители были против свадьбы (мб свадьба по залету была). Умнее бати, но тоже не гений. Верит в плохую энергетику, духов и прочую хрень. Считала солнце планетой""",
            u"""адекватная женщина 41лвл, иногда может депрессовать и накручиваться. По ее словам, одно время размышляла о выпиле. Курит с 17-ти лет (непостоянно, нерегулярно, по настроению), в то же время переехала в общагу и начала выпивать в компаниях. Сейчас убивается, мол "за всю жизнь ничего, кроме семьи, не добилась, работа говно, зарплата говно, дачи нет (это ее мечта, ну дача)". Работает какой-то там управляющей, въебывает, вроде в месяц около 30к. Два высших химическое и экономическое.""",
            u"""милая, забитая, тихая женщина. По характеру тряпка, но не истеричка. 30 с хреном лет моет посуду в учебных заведениях. Любит копаться в земле — сейчас вроде постоянно возится на даче с какими-то грядками.  Изменила бате, то ли во время свадьбы, то ли сразу после — за это и страдает все почти 30 лет замужества.""",
            u"""инжерен геофизик/юрист второе, по специальности почти не работала, обычно сидела во всяких отделах кадров. Нормальная мамка, не ватная, всегда хотела чтобы батя увез нас в какуйнить Канаду, специальность и мозги позволяли.""",
            u""" типичный пример того что бывает с прилежными отличницами.
            Закончила школу мухосрани с золотой медалью, получила джва высших образования (оба из которых сейчас не нужны) в союзе работала Каким-то там замкомом по чему-то там.. Короче была высокой шишкой, но из за того что была вся такая примерная и правильная, как только начался пиздец после 91 года сьебалась (Тот хуй что встал на ее место после отжал себе завод и построил особняк недавно).
            Сейчас работает в офисе за ~24к, тянет семью, курит, но пытается это скрыть.""",
            u"""закончила вуз, работает в серьёзной фирме. Карьеристка. Судя по её рассказам была довольно стервозной. До того как начала жить с батей была замужем три раза, все трое сбежали, один аж на тот свет. Батя видать укоротил её нрав. 8 лет вместе. Угорает по нью-эйдж. Тебя никогда не пыталась всопитывать и боялась лишний раз накричать""",
            u"""35 лет, не пьет и не курит, диабет. Работает учителем английского в младших классах и иногда ездит в Финку подрабатывать массажисткой.  Отношения у вас просто пиздец и ничего больше не скажешь.
            Обожает фотаться, прикольчики на одноклассниках и регулярно ездит к ебырю в другой город, очень бесится, когда бабушка обвиняет мамку, что та не уделяет времени своим детям,""",
            u"""таки осилила кандидатскую в лесотехническом (лол), в дивиностые занималась торгашеством, потом работала в юридической фирме. Не выдается умом, но очень адекватна, осторожна, имеет чутьё и со всеми вообще хорошо обращается. Алсо альпинистка.""",
            """обычная истеричка, работающая терапевтом в црб с завышенным чсв и стремлением время от времени снимать стресс скандалами. За батю замуж вышла скорее всего из-за квартирки, так как была практически без жилья, ибо бежала из Казахстана после развала совка и гонений на русских. Убеждения обычные, совковые, патологически ненавидит хачей и евреев. Неплохо так спорит с людьми.""",
            """идеальная пара отцу. Тихая, спокойная, умная, интеллегентная женщина, родила обдумав и проживя с отцом два года, в 28 лет. Атеистка. Политические взгляды не такие ярко выраженные, как у отца, но все равно, по сути, либерал. Читает еще больше отца, вообще без книги в руках ее почти не вижу. По молодости была той еще хиккой: одна подруга, и то с ней связь уже утеряна, отец был ее первым серьезным партнером и всякое прочее, няша-стесняша, короче. По образованию архитектор, окончила училище. Потом пошла в МГУ на филфак, но из-за работы пришлось бросить. Пишет потрясающие стихи и романы и Уотказывается публиковаться.""",
            u""" обычная баба позднего совка, отличница, вышла замуж за батю в 18, че там у них в молодости было я не знаю, в 24 родила меня. Когда батя откинул коньки она пошла работать и тащила тебя еще 10 лет. Уже не такая активная, начинает чаще творить хуйню, к моим советам не прислушивается. """,
            u""" ненаскакавшаяся на хуйцах толстуха, воспитывает меня полукорзиной, любит смотреть кино, залипать в соцсетях, где ищет новых ебырей каждую неделю, постепенно приобщается к интернету. Алсо, 45 лвл.""",
            u"""выполняет обязанности бухгалтера, но получает зарплату зав.склада, пьет, любит мультики, любит воспоминания о советском союзе, поебалась с отцом в 10 лет""",
            u"""тихая, по-хорошему не очень умная женщина, гуманитарная вышка, заботливая. Домохозяйка. Была гиперопечной, пока ты был мелкий. Пьет по праздникам.""",
            u"""характер мягкий, но когда злится, боюсь ее больше, чем всех демонов ада. Заткнёт за пояс половину мужиков, заботлива, мудра, имеет живой ум, но часто притворяет дурой. Была жената, когда познакомилась с отцом, ушла с ребёнком. Закончила тех-вуз в совке, в 90-х получила экономическое и бухгалтерское образование. Была директором, главбухом, финаналитиком половины универмагов в Москве, сейчас просто бух в какой-то логистической конторе. Тонкий психолог на личном опыте, может вырулить любые конфликты. Заботлива, но под юбку никогда не прятала.""",
            u"""фельдшер, закончила 9 классов и учагу, но на то были причины, так как тогда её мать умерла, батя съебал, она осталась одна со своей сестрой четырнадцати лет. Очень адекватная, почти не ебёт мозги, несколько глупее бати.""",
            u"""поехавшая на религии,четырежды отлежавшая в психушке дура.не работает,висит у бати на шее.пока я был в сосничестве постоянно тебя пиздила за просто так(наверное по этому у тебя так плохо с тнями?)""",
            u"""старше бати. Младший научный сотрудник на одном предприятии в нашем мухосранске, хотя по образованию (SIC!) логопед. Умнее бати и человек она очень хороший, хотя тоже много говна в голове.""", 
            u"""минидиктатор с ручным мужем-корзинкой. Раньше работала лаборантом на ТЭЦ, потом уволилась и пришла к успеху в сфере ремонта офисной техники Йоба-дирехтор. Раньше всех дрочила по чём зря, но потом одумалась и вообще болт забила. Обладатель большой тупой и старой собаки.  Неистово гордится тобой по настроению и перед гостями. Пытается от тебя избавиться: ко-ко-когда себе семью заведёшь???!!. Имеет разряд по водному и пешеходному туризму.""",
            u"""советская отличница, познакомилась с батей - начала ставиться, залетела - завязала. Когда залетела второй раз - бросила курить. Ебануто-религиозная: то бог все видит, иди поставь свечку в церкви, то славянские боги рулят, перун вперед. Бухает, пытается не палиться перед мужем, недавно подсела на одноклассники, иногда хочет выпилиться, походу изменяет.""",
            u"""охранник на заводе, 52года, почти 30 лет проработала проводницей на одном из самых элитных поездов Рашки. Не любит Путина, знаменитостей, богатых, башкиров, татаров, таджиков, глупые имена, жирных баб, жирных мужиков, пиво, телевидение, русскую музыку, да и вообще все русское.Худая, почти не ест обычную еду, целыми днями пьет кофе со всякими сладостями и смотрит сериалы, которые заставляет тебя скачивать, весь хард забит ими. Каждый раз, когда приходит с работы, пилит охуительные истории, как она всех ненавидит. Курит лет с 20.""",
            u"""учитель истории. Не курит, пьет шампанское/вино раз в пять лет по праздникам. Хуярит на даче, пиздюком тоже туда приходилось ездить, помогать. Строга, часто истерична, всё принимает близко к сердцу, свободное время - за телеком, отсюда и очень "ватниковские" политические и региозные взгляды, ведь она недавно потеряла двух сестер, лучшую подругу""",
            u"""инженер-строитель, работает в одной голландской международной корпорации. Не курит, не пьет, достаточно религиозна. Хорошо начитана и образована, но тем не менее иногда верит в откровенную хуиту. Может поистерить, но в целом характер веселый.""",
            u"""начальник смены на местной ТЭЦ, боксер по-молодости, имеет некоторое кол-во "авторитетных" знакомых в разных частях России, от которых в свое время отстранился с его слов из-за любви к моей матери, из-за чего одно время по-пьянке немного бугуртил. Дохуя сообразительный в бытовом плане мужик, охуенный спец в электрике, электросетях. В/О получил после сорока, бросил пить, сейчас почти все время проводит с маман на даче.""",
            u""" в принципе хорошая и адекватная женщина, но с перегибами. Склонна к истерикам и любит срываться на тебе. Однако смогла в одиночку вывезти нас в 90е, за что ей спасибо. Умная, начитанная но недалекая. Следит за собой и старается быть в тренде. Не пьёт, но курит.""",
            u"""медсестра в частной поликлинике. Добрая и понимающая женщина, училась на психолога, но забросила. В молодости гуляла, имела охуительную внешность и отшивала толпы пиздолисов, но потом остепенилась. Немного ПГМнутая, имеет богатый лексикон, любит классическую литературу и когда-то увлекалась философией. Неравнодушна к кошкам.""",
            u"""гиперопечная жирная женщина, вышка на химика-технолога, работает инженером по ремонту, вместе с батей. ПГМнутая, верит в живую воду, энергетику, СТРУКТУРУ ВОДЫ и прочий бред имени НТВ"""
            u"""типичная медсестра, лол, любит смотреть русские сериалы, за всю жизнь прочла 3,5 книги, наверное. Любит крепкое словечко, за что как-то получала бамбулей от бати. Не такая ПГМ-нутая как он. Любит цветы, кота, печь тортики и готовить разное хрючево. Очень завистливая и вспылчивая, от неё ты постоянно терпишь гиперопеку. Но она хорошая мать."""
            u"""всю жизнь после универа работает чиновницей в государственном ведомстве. Даже не пытается строить карьеру. Книг не читает вообще, смотрит какую-то парашу по телевизору. Недавно батя подсадил её на судоку, чтобы не разлагались мозги, лол. Сидит вечерами - разгадывает""",
            u"""56 лет, логопед, тащит всю семью, зарабатывает больше всех (на одной работе около 20к, а на второй - около 10к, лол). Плюс её пенсия. Подрабатывает, ставя речь людям за отдельную плату, ходит в фитнесс-клуб. Водит авто. Выглядит моложе своих лет.""",


    ]
    def at_object_creation(self):
        self.cmdset.add(CmdSetTest)
        self.locks.add("call:false()")
        self.db.npc = True
        self.db.desc = random.choice(self.descriptions)

    def at_object_receive(self, obj, source_location):
        self.execute_cmd("say Хороший сына растет, спасибо за %s, %s!" % (obj, source_location))

class YourDad(Object):
    descriptions = [ 
        u"""еврей старой закалки. Не жлоб, но с жлобинкой такой, небольшой но чувствующейся. Пришел к успеху в 90е когда тусил с бандитами, я так понимаю он там чисто числился и иногда их по домам развозил, но тем не менее пацаны пошли в гору вплоть до губернаторства и прочих чинов - и батю с собой потащили. Главный врач больнички областной.""", 
        u"""альфач, который постоянно бухает и учит тебя жизни, хотя на самом деле просто самоутверждается. Пограмист и вообще довольно неплохо разбирается в интернетах, считает себя не ватником а норм поцреотом, хотя на самом деле обычный ватник. Упрекает тебя в том, что нету бабы и друзей, но считает тебя вроде как довольно умным. На самом деле он не очень-то и глупый, просто обычный конформист, хотя в молодости был анархистом и слушал Монгол Шуудан, лол. Еще когда напьется часто говорит что мол вот настоящая жизнь ты от нее никуда не убежишь, но ты ему не веришь.""",
        u"""58 лет, бывший суворовец, ныне военный пенсионер в чине капитана. Усат. Раньше был подкачан, спортивен, бил солдат, которые на него выёбывались. Шарит в электрике, подрабатывал в 90-е кем придётся, работал на заводе полиэтиленовых и пластиковых изделий, был мастером смены. Потом на другом предприятии в ОТК (производство бытовой техники). Сейчас в автосервисе работает за гроши автоэлектриком (почти каждый день на работе, а заказов почти нет - вот и выходит около 15к). Водит ниссан 2004 года выпуска (раньше на нём мама ездила, но он ей отдал свой фольксваген).""",
        u"""Батя раньше был весьма успешным и руководил филиалом весьма крупной фирмы в нашем городе. Когда начался кризис в 2008ом, он уволился с работы и пару лет сычевал. Сейчас работает на одном оборонном предприятии. Его подчинённые - быдлота и он начинает скатываться до их уровня. Шансончик начал слушать, лол. Матом чаще ругается, хотя это пиздец неприятно слушать от отца. Ну, при мамке не матерится, лол. Постояно смотрит телепередачи из цикла "В мире хохлов", но достаточно адекватно смотрит на это всё, лол.""",
        u"""когда-то зотел стать лётчиком, стал экспедитором на поездах или что-то в этом роде. ПГМ овер 9000 - почти любой разговор дожлен перейти в духовное русло. Батя хохол как и все мы, но думаю если бы рос в рашке был бы типичный ватан. Не курит, много не бухает, вообще как на свои годы сравнительно неплохо выглядит, но ноги варикозные пиздец, думаю скоро с этим будут большие проблемы. Из увлечений - недавно перейнял у деда увлечение ПАСЕКОЙ. Всегда говорит чтобы был мужиком, иногда "что ты как баба". Иногда пиздит мамку. Есть 4 родных сестры. Я его уважаю и боюсь, перейнял многие черты характера""",
        u"""инженер-асушник, доработался до зам нач цеха тепловой автоматики, в начальники не пустили, вышки нету. Пил запоями, пока торпеду не вшили, теперь не пьет ( уже лет 5-6 ). Изменял мамке регулярно, раньше был женат на другой кажется.""",
        u"""мастер на все руки, может почти в любую рабочую профессию: токарь, слесарь, столяр, электрик, кузнец, сантехник, монтажник, маляр, грузчик, механик. В молодости был кандидатом в мастера спорта по тяжелой атлетике, здоровый пиздец просто. Любит эрпоге(сейчас Герку второй раз проходит), фэнтези, увлекается холодным оружием и сам его делает. Атеист, изучает научпоп, последнее время постоянно смотрит политоту и мамкиных историков на ютубе, что тебе очень не нравится. Очень работящий мужик, не пьет и не курит, девственности лишился в 30 лет с моей мамкой.""",
        u"""начальник смены на местной ТЭЦ, боксер по-молодости, имеет некоторое кол-во "авторитетных" знакомых в разных частях России, от которых в свое время отстранился с его слов из-за любви к мамке, из-за чего одно время по-пьянке немного бугуртил. Дохуя сообразительный в бытовом плане мужик, охуенный спец в электрике, электросетях. В/О получил после сорока, бросил пить, сейчас почти все время проводит с маман на даче.""",
        u"""дервенский труженник, тракторист и прочий работяга. Не осне образован, не работает, рыбачит и кормит скотину, по дому кароч хуяит. Раньше адово бухал и пиздил мамку""",
        u"""подкаблучник, и жирный хуй. всю зарплату в дом, все покупки с разрешения мамки. такой ущерб. всю жизнь проработал на говнозаводе за копейки, хотя мог бы пойти в связисты после армии, а не в ебаный инст на химика. телец""",
        u"""водила межгородних автобусов. Простой мужик, не пьет, курить бросил 21 год назад, свободное время проводит за быдлотелеком. Ленив, похуистичен, видимо в этом я в него вырос. Помогает с деньгами раз в месяц""",
        u"""эталонное небыдло-гуманитарий. Имеет много прочитанных книг (полный шкаф из него 1/3 философия). Очень хорошо ведет аргументированный спор, упорный и настойчивый Ерохин на руководящей должности. Спортсмен, красный диплом и медаль в школе.""",
        u""" имеет вышку, считает себя элитой, несколько лет назад поднялся на работе, но потом его опять понизили за то что не лижет зад начальству, не приемлет точку зрения, противоположную ему. Два года назад закодировался. Ранее был женат, имеет дочь овер30лвл""",
        u"""старый пидор на пенсии, в молодости женился на мамке, которую привез с Украины в сибирские пердя, сделал двоих детей и съебал в закат в начале 90-х. Был ментом, уволили из органов за избиение подследственных, но ментовская лживость и гниль остались навсегда. Женился на городской шлюхе, сделал ей ребенка, спустя время тоже съебал, женился снова и снова на шлюхе, ей сделал ребенка инвалида и спустя 10 лет снова съебал в закат. Сейчас опять живет с твоей мамкой.""",
        u""" за 50, лысый, стареющий бизнесмен, который бизнес этот ваш и так не наладил, собирается всё бросить и дожить годы с теперешней женой помоложе. По образованию биолог-охотовед, характер отвратительный, жаден как еврейский чёрт, последние 2 пункта унаследовал от него, хотя сам полная его противоположность. Мракобес, верит в антинаучную хуиту, вроде пришельцев и экстрасексов. Ну и в связи с последними событиями, тоже начал путена считать хорошим президентом и стражем россиюшки от западного нашествия.""",
        u"""Хронический нытик. 42лвл. Закончил 8 классов. Из-за ссоры с куратором ушел из шараги. 15 лет работал охранником на стоянке. Сейчас его пристроил друг соучредителем в какую-то контору. Жмот. Считает каждую копейку. Изменял, из-за чего родители расходились на год. ПГМ-нутый. При этом верит всяким гадалкам.""",
        u"""полицейский, заместитель начальника отдела. Бывший лётчик, точнее инженер, или что-то такое, типа третьего пилота, который смотрит за состоянием самолета, сам тоже в качестве пилота летал. В ментовку пошёл из-за того, что аэродром закрыли. В общении интересен, любить играть в игоры""",
        u"""характер жёсткий, нордический. Армия, стройки-автосервисы, юридическая+экономическая вышка в 38. Приехал с матерью в Москву с двумя чемоданами из без знакомых. Если не по его, то пиздец всему и всем. Имел бизнес, пока какой-то из кризисов 2000-ных не сломал всё к хуям. Из-за бизнеса стал немножко поехавшим на голову в плане нервов (неврастеник). Знает и умеет кучу всего. Перечитал тонны книг от всяких Ницше-Кастанед-Эко-Достоевских-Кантов-Кафк-Гёт до Гарри Поттеров и Хроник Нарнии. Охуительные аналитические способности. Талант в рисовании и музыкальный слух. Тонны жизненного опыта. Пиздецкий угнетается мыслью, что проебал кучу возможностей/не сделал/не довоспитал/не додумал и т.д.""",
        u"""далеко за 50, техническая вышка, был предпринимателем, продал бизнес, хиккует, зарабатывает в инете, иногда играет в игоры, смотрит сериальчики с маман. """,
        u"""хотел бы чтобы был совок(за то, что все было усреднено), любит три мушкетера(книгу), слушает Высоцкого, любит футбол""",
        u"""Батя -- типичный сельский тупой агрессивный быдлан, закончил 8 классов школы, с 10 лет курит, верит в жидорептилойдов на дне байкала, на вопрос "за сколько солнце обращается вокруг земли" отвечает "откуда я знаю, моя задача -- зарабатывать деньги". Изменял/изменяет. Иногда приходит домой нажравшись. Рассказывал, что в армии работал охранником в тюрьме и кого-то там завалил. Алсо, имеются какие-то наколки вроде тюремных. Скучает по советскому союзу.""",
        u"""тупой селюк. 8 классов образования, курит с армии, зато бухает лет с четырнадцати, хронический бронхит с десяти. Имеет ребёнка на стороне, о котором пару лет назад узнал. С тем ребенкома тому уже 20+ лет ни он, ни я, не знакомы. Изменяет. Каждый день пьяный с работыкогда работает. Собственно, отцом я его не считаю. Его отец умерне удивительно, мой батя восьмой ребёнок в семье когда ему было года два. Его воспитание ограничивалось пьяными обещаниями завтра же отдать меня в секцию на единоборства. Так и не отдал. Я его пиздил пару раз.""",  
        u"""Нечто вечно всем недовольное, лежащее на продавленном диване в дырявых трениках с отвисшей мотнёй. 
В руках бульварная газета и пульт от телевизора с транслируемым политическим ток-шоу. 
Отцеподобное существо любит царственно почёсывать пивное брюхо, обожает пятничный преферанс и вяленую воблу, 
готово до хрипоты в горле спорить о преимуществе блесны над мормышкой и макушатника над дождевыми червями. 
Профессор кроссвордогадания летом выходит играть в домино прямо в домашних тапочках, бритьё подмышек и дезодоранты считает уделом педерастов. 
Сортирный генерал категорически отказывается пользоваться обувной ложкой и ситечком для чая. 
Жлобатько не пьёт шмурдяк в баре биллиардного клуба, а заранее накачивается рядом в киоске-наливайке, где гранчак аналогичной бурды на рубль дешевле. 
Диванный князёк кроет жену нецензурной бранью за невымытую тарелку и слабо нагретый ужин, 
хотя сам не менял носки три недели и мылся «когда последний раз горячая вода в кране была». На бойлер денег скопить надо, экономить на пойле придётся, устанавливать его потом — гембель, сопоставимый по объёмам со строительством БАМа.
""",
       u"""алкаш 42лвл. Непостоянный, пиздаболит частенько. Когда трезвый - еще более-менее, но выпьет - доебывается до всех, выебывается, нажирается в хламину и становится агрессивным. В целом он пиздатый, но опять же, только когда трезвый. А так, когда он он пьяный - типикал вата-поцреот. Зато ололо-трудоголик, въебывает сам на себя в автосервисе и не знаю точно сколько получает, но что-то около 70к. Высшее образование хз какое, но он автомеханик по профессии.""",
       u"""алкаш. Строитель. Окончил соответствующую шарагу. Всегда бухал, сколько ты его помнишь. Скандалист и истерик, когда напьется. В детстве пиздил не раз по пьяни, пытался убить. Сломал матери руку. Увлечений не имеет, но по сезону рыбачит, мастерит и ремонтирует хуйню всякую, чинит двери, которые по пьяни же и выбивает. Сейчас, вроде бы, поутих — здоровье не то. """,
       u"""- безработный алкаш. Днями только и делает что смотрит зомбоящик и ходит на рыбалку. 1-2 раза в год съебывает куда-то на стройку на месяц-два. Затем за 2 недели все проебывает и снова нихуя не делает. Временами срется с мамкой, так как её бесит то что он месяцами пинает хуй, но ему похуй.""",
       u""" инженер геофизик, с детства был радиолюбитель, как только получил вышку так и получил работу по распределению, потом кое где случилась война и в 92том вместе с беременной женой пришлось покинуть родной город продав хату за бесценок бабка с дедом еще долго там жили не смотря на весь пиздец переехав в родной город мамки и живя там до нулевых, на хату удалось скопить буквально за 98-01 работая на севере. В меру ватный, юморист, гомофоб, вечно что то собирает, то электросварку, то усилок какой.""",
            u"""на пенсии. Москвич, закончил 8 классов и какую-то хуйню, сьебался в 90 в мухосранск потому что первая семья развалилась и встретил твою мамку.
            Работал на дохуище разных работ, много чего умеет. Сейчас проебал все свои удостоверения и работать по специальности по черному уже не может.
            Работает охранником за 5 к +5 к пенсии.
            Из себя представляет либерала антикоммуниста, читает Эхо Москвы и прочее, ненавидит Путлера, любимая тема для разговора - куда катиться Раиссия. Курит с 16 лет, сейчас перешел полностью на электронку.""",
            u"""достаточно крутой и умный дядька, из хорошей советской семьи (дед - полковник милиции в СССР), окончил хороший по тем временам институт, правда военный. Нехило поднялся в 90-е, сейчас имеет свой бизнес в ДС, связанный с арендой крупных помещений плюс строительство. Из минусов - в силу автономности бизнеса имеет кучу времени, которое тратит на спорт, что в купе с военным институтом сделало из него просто робота по протиранию полочек, пробежек, таскания мебели, поездок туда, сюда, направо, налево. Короче, шило в жопе, лучше к нему вообще не подходить, иначе сам окажешься в процессе. Достаточно властный и сильный морально и физически.""",
            u"""Батя закончил ПТУ, по малолетке сидел за вооруженное ограбление. В 90х был одним из первых лиц в топовой бандитской гильдии города. Все проебал из-за наркоты и бухла. Провел лет 10 в резервации в глухой деревне после бандитских разборок. Бросил употреблять/бухать, потихоньку выбрался из говна. Сейчас работает, задротит в WOT, двачует уже года 3. Несмотря на все что было - он ахуенен.""",
            u"""сказочный долбоёб, не осилил кандидатскую в лесотехническом, копротивляется Обаме на форумах за Новороссию (и искренне верит, что его охуительные советы читает Медведев), делает вотку, считает себя фелозафом. Болтлив и мелочен. Это от неудач. Карлан.""",
            u"""охуенный технарь с кучей изобретений, бывший баскетболист, алсо препод матана, в 70 лет увлёкся нейробиологией и по хардкору её изучает (начал с химии, через год штудировал эмбриологию, сейчас добрался до когнитивной нейронауки), мозг вообще не ослабел с возрастом. Котирует классическую музыку, коей накачал 4 терабайта (нет, акустика не Гениус), снукер и шахматы. Имеет минус: рядом с ним чувствую себя похожим на батю.""",
            u"""молчаливый и угрюмый крепкий мужик, раньше (мать говорила) по штанге угорал. не охотник - но ружье и карабин с оптикой в сейфе держит. ни разу не видел что бы бухал, пьяного тоже не видел. не курит. горный инженер - работает вахтами. после вахты спит дня два. матерится сильно - но только дома или когда друзья его приходят. когда дома отоспится - постоянно вытаскивает гулять/на спортплощадку/на великах кататься/футбол там и прочее. запрещает матери купить телевизор.""",
            u"""служил, ликвидировал последствия аварии на ЧАЭС. При советах имел много всего, благодаря деду. Умудрился перед амией проиграть в карты волгу. В 90х мутил бизнес, нихуя не взлетело. Проебал все квартиры, живе в поселке возле мухосрани. Нихуя не имеет, настрогал кучу детей, хочет наладить между нами общение.""",
            u"""-53года, модный и стильный мужик не сомторя на свой возраст, очень опрятный, любитель шопинга в брендовых магазинах, любитель съездить в клуб на выходных с друганами не смотря на свой возраст, в 90-х "мутил дела" и был богатым пока по форстмажорным обсоятельствам все не потерял(обида((()очень добрый, не мелоный не имеет привычки копить денег, АБСОЛЮТНО НЕ ПЬЮЩИЙ С 17-и лет.""",
            u"""жирноватый инженегр-строитель, 20 лет проишачил в сму, после развала совка за 3 копейки, потом оно таки закрылось лет 7 назад, и пошёл он батрачить по 12 часов на частника, но хоть лавэ стал зарабатывать. Очень любил бухать и читать фэнтези до встречи с моей мамашей, она его ото всего отучила, и он превратился в обычное аморфное приложение к телевизору, но эрудированность осталась, много интересного мне рассказал.""",
            u"""очень здоровый мужик 48лвл, никогда в жизни не работал, бандитствует. В молодости был байкером, хулиганом, имеет альбом с фотками голых баб которых он ебал в молодости. Очень большой, сука, альбом. Достаточно умен для того что бы построить дом и читать книги. Ненавидит всяких начальников, власть и армию, селюков тоже ненавидит. Любит драться с людьми, бил несколько раз женщин, один раз отхуярил какую-то бабку.""",
            u"""инженер, не доучившийся в свое время потому что нужно было обеспечивать семью, потому что меня родили в 20 лет. До 30 с хером лет работал на автосервисе, ставил сигнализации и прочее доп. оборудование. Получал неплохо, но на семью все равно было мало, потом по знакомству ушел работать на какую-то свалку, стал кем-то типа менеджера, начал получать действительно хорошие деньги. Пьет по 2-3 банки пива ежедневно, по вечерам смотрит в телек, по выходным спит и бухает. Очень тихий интроверт, практически не разговаривает.""",  
            u"""советский интеллигент во всей своей красе. Читал, наверное, все, что можно было прочитать, дико угорает по научной фантастике, на этой почве с мамкой на курорте и познакомился (она ехала в автобусе и читала Стругацких). Работает инженером на заводе, либерал, атеист. По млодости был коммунистом, но утверждает, что это был молодой идеалистический порыв. Бородат, приятен внешне. Немного агрессивен, очень громко разговаривает и очень эмоционален. При все этом, в молодости был довольно шабутной и альфовый: всякие пьянки-гулянки, тянки и так далее. На данный момент основную часть свободного времени проводит читая или смотря ящик, или болтая с мамкой. Еще из лего всякую хрень недавно начал строить.""",
            u"""Батя-типичный яппи мухосранского разлива. Медик. обожает рассказывать про курорты Египта и Греции. Про коко илитныое бухло говорить может часами. Ездит на жопеле инсигния который я перехватываю у него при первой же возможности. Дрочка на машину просто лютая. Любит историю, читает книги про армию наполеона и фашиков. Склеили с ним все танчики вермахта. Чем старше становится, тем добрее.""",
            u""" С одной стороны, довольно умен, и любой твой пиздеж распознает на первом слове или взгляде, серьезно. С другой - ему пиздец сложно что-нибудь доказать. Закончил технический вузик, на программиста учился, вроде(по крайней мере, дипломной у него было написание какой-то фигни для управления какой-то спутниковой фигней. На ассемблере.). Сейчас эникеет.""",
            u"""Гонял по вене. Пока я был маленький, часто варил дома, закрывшись на кухне со своими корешами. Помню мерзкий запах. Потом я подрос и на похуе светить передо мной ширевом уже не мог. Но часто приходил домой уебошенный или бухой, пиздил мамку. Зарабатывал воровством и, наверняка, другим мелким криминалом""",
            u"""всю жизнь алканил, проебал все полимеры, подпортил знатно этим жизнь всем близким. Нихуя в жизни не добился и не получил. Сейчас пить перестал, вроде жизнь благодаря этому наладилась и получает неплохую зп.""",
            u"""43 года вроде, вместе живем почти 5 лет вроде, приятный, но бывает раздражающим, ибо не всегда воспринимает чужое мнение. Курит с 25, не пьет(раз в неделю пиво). Многое умеет. Заведующий/главный инженер-электрик, зп -25к. 7/10.""",
            u"""Был нитакимкакфсе, в детстве дохуя упарывал футбол, после этого упарывал гитару, бухло и тёлочек, был настоящим альфачом. До мамки был в ещё одном браке. Учился в театральном в соседнем миллионнике, на режиссёра, работал по специальности всего процентов 30 от всего времени, остальная работа - охранником, охранником на севере, на вахте, бодигард у какой-то важной шишки. Приносил боевой ПМ домой, учил тебя его разбирать-собирать.""",


    ]



    def at_object_creation(self):

        self.cmdset.add(CmdSetTest)
        self.locks.add("call:false()")
        self.locks.add("get:false()")
        self.db.npc = True
        self.db.desc = random.choice(self.descriptions)

    def at_object_receive(self, obj, source_location):
        if obj.key == "травы":
          self.execute_cmd("say Ой, мне нужно в туалет")
        else:
          self.execute_cmd("say Путин - лучший президент!")

    def at_say(self, speaker, message):
          print speaker + " say " + message
          if (message == u"Батя ты лысый"):
                self.execute_cmd(u"say Ща пизды дам")


"""
класс с лолей

потом объевляем подоный класс

copyright 08.09.15
"""
class T_Loli(Object):
    """
    This implements a simple Object using the talk command and using the
    conversation defined above. .
    """	

    def at_object_creation(self):
        "This is called when object is first created."
        # store the conversation.

	CONV_loli = {"START": {"text": "Привет анон. Я %s. Добро пожаловать на Мудач. Снова." % self.key,
                  "links": ["i1", "i2", "i6","END"],
                  "linktexts": ["Кто такие лолли?",
                                "Ты любишь конфеты?",
                                "Что такое Мудач?",
                                "Пока."],
                  "keywords": None,
                  "callback": None},
        "i1": {"text": "Лолли это маленькие девочки. Они миленькие и беззащитные.",
                  "links": ["i2", "START", "END"],
                  "linktexts":["Ясно. Ты любишь конфеты?",
                  			   "Хочу еще кое что спросить.",
                               "Ясно. Пока"],
                 "keywords": None,
                 "callback": None},
        "i2": {"text": "Очень люблю. Дети ведь любят сладкое! А что?",
                 "links": ["i3", "END"],
                 "linktexts": ["Знаешь, у меня есть конфеты, давай трахаться?",
                               "Да не... ниче. Показалось. Пока"],
                 "keywords": None,
                 "callback": None},
        "i3": {"text": "А конфеты у тебя шоколадные?",
                 "links": ["i4", "END"],
                 "linktexts": ["КОНЕЧНО!",
                               "Нет. Только 'Рачки'."],
                 "selectcmds":[CmdChoco,None],
                 "keywords": ["1","2"],
                 "callback": None},
        "i4": {"text": "P-Put it in me, senpai... (*^.^*)",
                 "links": ["END", "i5"],
                 "linktexts": ["[Закончить]",
                               "У меня еще трюфели есть."],
                 "selectcmds":[None,CmdTruff],
                 "keywords": ["1","2"],
                 "callback": None},
        "i5": {"text": "Только не туда, семпай... (*^o^*)",
                 "links": ["END"],
                 "linktexts": ["[Закончить]"],
                 "selectcmds":[CmdSetStr],
                 "keywords": ["1"],
                 "callback": None},         
        "i6": {"text": "Мудач это наш Муд-маня-мирок для анона по мифологии имиджборд. Здесь все твои друзья. MUD - многопользовательский текстовый квест. Если хочешь, можешь познакомиться поближе с нашим проектом.",
                 "links": ["i7","i8","i9","START"],
                 "linktexts": ["Где почитать F.A.Q?",
                 			   "Как к вам присоедениться?",
                 			   "Расскажи поподробней об этом мире",
                 			   "Хочу еще кое-что спросить."],
                 "keywords": None,
                 "callback": None},
        "i7": {"text": "F.A.Q. для новичком есть в нашей Wiki на Github. Пройди по этой ссылке - https://github.com/op-hui/mu2ch/wiki и там ты найдешь то, что искал.",
                 "links": ["i8","i9","START"],
                 "linktexts": ["Как к вам присоедениться?",
                 			   "Расскажи поподробней об этом мире",
                 			   "Хочу задать еще пару вопросов"],
                 "keywords": None,
                 "callback": None},
        "i8": {"text": "Чтобы к нам присоедениться нужно пройти по ссылке - https://github.com/op-hui/mu2ch. Это наш репозиторий. В ReadMe.md описано, что нужно чтобы стать творцом миров.",
                 "links": ["i7","i9","START"],
                 "linktexts": ["Где почитать F.A.Q?",
                 			   "Расскажи поподробней об этом мире",
                 			   "Хочу задать еще пару вопросов"],
                 "keywords": None,
                 "callback": None},
        "i9": {"text": "Пока что наш маня-мирок ограничиваеися квартирами анона и общим коридором. Если у тебя есть предложение или ты нашел баг то оставь это здесь https://github.com/op-hui/mu2ch/issues",
                 "links": ["i7","i8","START"],
                 "linktexts": ["Где почитать F.A.Q?",
                 			   "Как к вам присоедениться?",
                 			   "Хочу задать еще пару вопросов"],
                 "keywords": None,
                 "callback": None},
        "i10": {"text": "Ну ты и тварь... у тебя нет конфет...",
                 "links": ["END"],
                 "linktexts": ["[Закончить]"],
                 "keywords": None,
                 "callback": None},
         "i11": {"text": "Ну и тварь же ты... у тебя нет трюфилей...",
                 "links": ["END"],
                 "linktexts": ["[Закончить]"],
                 "keywords": None,
                 "callback": None},                     
        }


        self.db.conversation = CONV_loli
        self.db.npc = True
        self.locks.add("call:false()")
        self.locks.add("get:false()")
        self.db.desc = "Маленькая девочка. Одета в футболку и юбку. Можно вступить с ней в диалог при помощи команды talk или на русском 'ск'. Любит 'шоколадные конфеты' и 'трюфели'"
        # assign the talk command to npc
       #self.cmdset.add_default(TalkingCmdSet, permanent=True)

"""
команды для дилога

"""

class CmdSetStr(Command):
	key="1"
	locks = "cmd:all()"
	
	def func(self):
		caller = self.caller
		caller.db.str = 5
		caller.db.agl = 5
		caller.db.vos = 5
		pantsu = create_object(settings.BASE_OBJECT_TYPECLASS, "Детские трусики", caller, home=caller)
		talking_to = caller.search(caller.db.last_talk_with, location=caller.location)
		pantsu.db.desc = "Трусики принадлежат: %s!" % talking_to.key
		self.menutree.goto("END")

class CmdChoco(Command):

	key="1"
	locks = "cmd:all()"

	def func(self):
		caller = self.caller
		talking_to = caller.search(caller.db.last_talk_with, location=caller.location)
		sweets = caller.search("шоколадные конфеты", location=caller)
		if not sweets : 
			self.menutree.goto("i10")
		else : 
			self.menutree.goto("i4")
			sweets.move_to(talking_to,quiet=True)

class CmdTruff(Command):

	key="2"
	locks = "cmd:all()"

	def func(self):
		caller = self.caller
		talking_to = caller.search(caller.db.last_talk_with, location=caller.location)
		sweets = caller.search("трюфели", location=caller)
		if not sweets : 
			self.menutree.goto("i11")
		else : 
			self.menutree.goto("i5")
			sweets.move_to(talking_to,quiet=True)
