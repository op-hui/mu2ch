Как сделать собственного npc:

код:
```python
from evennia import Object, CmdSet
from evennia import default_cmds

class CmdSetTest(CmdSet):
     def at_cmdset_creation(self):
         self.add(default_cmds.CmdSay())

class YourMom(DefaultObject):
    # Этот код выполняется при создании объекта
    def at_object_creation(self):
        self.cmdset.add(CmdSetTest)
        # Запрещаем призывать этого NPC откуда либо
        self.locks.add("call:false()")
    
    # Это код выполняется, когда наш объект получает от другого объекта предмет
    def at_object_receive(self, obj, source_location):
        # obj - сам объект
        # source_location - откуда объект был передан
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


