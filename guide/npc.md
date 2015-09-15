Как сделать собственного npc:

код:
```python
# -*- coding: utf-8 -*-

#Внимание первая строка должна быть именно такой
#Иначе питону плохеет от utf-8 русских символов

from evennia.mudach.typeclasses.npc import simpleNPC

class YourMom(simpleNPC):
    # когда персонаж что либо дайт Мамке, она благодарит его за это
    def at_object_receive(self, obj, source_location):
        self.execute_cmd("say Хороший сына растет, спасибо за %s, %s!" % (obj, source_location))
```

Создаем в директории mudach/typeclasses 
Файл npc.py 
```
mudach/typeclasses/npc.py
```

Далее заходим в игру:
и пишем:

```
@create Твоя Мамка:npc.YourMom
```

Теперь протестируем:

```
@create стакан воды
give стакан воды = Твоя Мамка
Твоя Мамка says: "Хороший сына растет, спасибо за стакан воды, anonymous!"
```


