Как сделать собственного npc:

код:
```python
from evennia import Object, CmdSet
from evennia import default_cmds

class CmdSetTest(CmdSet):
     def at_cmdset_creation(self):
         self.add(default_cmds.CmdSay())

class YourMom(Object):
    def at_object_creation(self):
        # here we add the cmdset
        self.cmdset.add(CmdSetTest)
        # we should lock the object so we can't
        # call commands on it from "the outside",
        # (only the npc itself should have access to
        # this command). This is done with the "call"
        # lock type.
        self.locks.add("call:false()")
    def at_object_receive(self, obj, source_location):
        self.execute_cmd("say Хороший сына растет, спасибо за %s, %s!" % (obj, source_location))
```

Добавляем в собственный новый класс объектов 
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


