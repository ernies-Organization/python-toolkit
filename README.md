
# python-toolkit
a toolkit of useful python scripts

# important
you are able to edit and use this in your code without consent from me  
(as long as you are not using it for illegal/inappropriate things)

this is licensed under the [MIT licence](https://github.com/ernies-Organization/python-toolkit/blob/main/LICENSE)

# projects
below are all the projects and instructions for them

<details>
  <summary><strong>all projects</strong></summary>

- <a href="#leaderboard-from-file">leaderboard from file</a>  
- <a href="#user-database-from-file">user database from file</a>  
- <a href="#password-generator">password generator</a>  
- <a href="#password-strength-checker">password strength checker</a>

</details>

---

## leaderboard from file
this is a leaderboard that allows you to:
- save a leaderboard to a file  
- load it  
- update the highest score for each player  
- print it in sorted order  

project file →  [leaderboard-from-file.py](https://github.com/ernies-Organization/python-toolkit/blob/main/leaderboard-from-file.py)

### setup
at the top of your script you need:

```python
import json
```

inside your editable variables section:

```python
LEADERBOARD_PATH = "leaderboard.json"  # File name for the leaderboard (must end in .json)
leaderboard_lenth = 10                # number of scores displayed
```

### add a score to the leaderboard
```python
record_result(name, rounds)
```
- `name` → the player's name  
- `rounds` → the score (must be above 0)

### print the leaderboard
```python
print_leaderboard()
```

[↑ back to top](#projects)
---

## user database from file
this is a full user account system that allows you to:
- create accounts  
- login  
- logout  
- delete accounts  
- change username  
- change password  
- and includes a full admin panel with extra tools  

project file →  [user-database-from-file.py](https://github.com/ernies-Organization/python-toolkit/blob/main/user-database-from-file.py)
### setup
at the top of your script include:

```python
import json
```

then set the database file:

```python
USER_DATABASE_PATH = "user_database.json"  # where all user data is saved
```

### start the system
call this to start the login script:

```python
user_login()
```

this will:
- load the user database  
- create the first admin account if none exists  
- start the login/signup system  

### features

#### normal user features
- change username  
- change password  
- delete account  
- logout  

#### admin features
- view all users  
- delete any user (except last admin)  
- promote/demote users  
- reset passwords  
- rename users  
- create new users  
- view user details  

### database format
the JSON file stores data like:

```json
[
    {
        "username": "example",
        "password": "examplepassword",
        "admin": false
    }
]
```

you don't need to manage the file manually —  
all saving and loading is done automatically.

[↑ back to top](#projects)

---

## password generator
this script creates a **secure random password** using python’s `secrets` module, and asks you which character groups you want to include.

project file →  
[password_generater.py](https://github.com/ernies-Organization/python-toolkit/blob/main/password_generater.py)

### features
- choose lowercase, uppercase, digits, symbols  
- must include at least one group  
- ensures **at least one character from each selected group**  
- uses secure randomness (`secrets.choice`)  
- fully shuffled output  
- automatically checks strength afterwards

### use
run the script and answer the prompts:

```
Include lowercase letters? (y/n): y
Include uppercase letters? (y/n): y
Include digits? (y/n): y
Include symbols? (y/n): y
Password length: 16

Your password is: mK$9vR!zLp#2Xw&Q
Password strength: Very Strong (score: 10)
```

[↑ back to top](#projects)

---

## password strength checker
this script analyses any password and gives it a strength rating + score.

project file →  
[password_strength_checker.py](https://github.com/ernies-Organization/python-toolkit/blob/main/password_strength_checker.py)

### scoring
#### length
- 16+ → +4  
- 12+ → +3  
- 8+  → +2  
- 6+  → +1  

#### character types
- lowercase → +1  
- uppercase → +1  
- digits → +1  
- symbols → +2  

#### penalties
- only letters or only digits → -2  
- all characters identical → -3  
- triple repeated character → -1  
- contains: `abc`, `123`, `qwerty`, `asdf` → -2  

#### rating
- 0–2 → very weak  
- 3–4 → weak  
- 5–6 → medium  
- 7–8 → strong  
- 9+ → very strong  

### example
```python
strength, score = check_password_strength("Example123!")
print(strength, score)
# Strong 7
```

[↑ back to top](#projects)

---

