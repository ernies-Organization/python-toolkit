# python-toolkit
a toolkit of useful python scripts

# important 
you are able to edit and use this in your code without consent from me (as long as you are not useing it for illegal/inappropriate things)
this is licenced under the [MIT licence](https://github.com/ernies-Organization/python-toolkit/blob/main/LICENSE)

# projects
below are all the projects and instructions for them

## leaderboard from file
this is a leaderboard that allows you to save a leaderboard to a file, display it and edit it

project file -> [leaderboard-from-file.py](https://github.com/ernies-Organization/python-toolkit/blob/main/leaderboard-from-file.py)

at the top you need to have: 
```
import json
```
in a place for editable varibles have:

```
LEADERBOARD_PATH = "leaderboard.json" # File name for the leaderboard (has to have ".json" at the end)
leaderboard_lenth = 10 # lenth of leader board displayed
```

add a resolt to the leaderboard in the code with:
```
record_result(name, rounds) 
```
show the curent leaderboard with:

```
print_leaderboard()
```


