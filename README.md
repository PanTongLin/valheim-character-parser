# valheim-character-parser
### Valheim character file (.fch) parser with load/save function in python
***
This repository is a parser for character file (.fch) of [Valheim](https://www.valheimgame.com/).  
And this is mainly migrate from parser of [ValheimCharacterEditor](https://github.com/byt3m/Valheim-Character-Editor/blob/main/ValheimCharacterEditor/Parser.cs).

You can eaisly load the character file in a single line and edit its profile, then also dump the modified one in one line.  
```diff
- ALWAYS REMEMBER TO BACKUP BEFORE YOU EDIT THE CHARACTER FILE !!!
```
This parser has been tried on **version 0.146.8**, and it also works on multiplayer mode.
***
A demo of changing all the skill level to 30 is shown in `main.ipynb`  
```python
from Character import character

char = character("player.bak.fch")
print(char)

for i in range(char.num_skills):
    char.skills[i]['level'] = 30.0

char.save('player.fch')
```
#### NOTE : It might need to adjust `character.file_size` and `character.data_len` yourself if you have edited any data in string format which also changes the size of character file.
