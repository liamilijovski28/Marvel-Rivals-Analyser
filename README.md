# CITS3403-Project
Agile Web Development Project

Welcome to Marvel Rivals Analyser, which will allow the user to compare their stats with friends to see who's the best superhero!

| Name      | Student ID | Github Username |
| ----------- | ----------- | ----------- |
| Adam Wright| 23381084 | Pineapples117 |
| Liam Ilijovski | 23349674 | liamilijovski28 |
| Izzy Xiong | 23666309 | Isheyyy |
| Adam Visser | 23881949 | UnexpectedParentheses |


# Marvel Rivals Basics
In Rivals, two teams of 6 players battle each other for control of an objective. Each player plays a character which is one of three classes – Duelist, Vanguard, & Strategist. Broadly speaking, Duelists job is to deal damage and defeat opponents, Vanguards are meant to absorb damage and stop their team from suffering and Strategists are meant to heal and buff their team.

Each game a user logs, they will submit the following statistics:

-Game mode (This project will support only either Quick Match or Ranked)

-Current Season (Is either 0, a positive integer, or a positive integer + 0.5)

-Character (who they played), 

-KOs (How many opponents they helped defeated through damage), Deaths (How many times they were defeated), 

-Assists (How many opponents they helped defeat through buffs), 

-Final Hits (How many opponents they did the final damage to defeat)

-Damage (Damage dealt to opponents)

-Damage Blocked (Damage the user took)

-Healing (Health restored by the user)


# Set up
```
Clone the Repository:

  git clone https://github.com/liamilijovski28/Marvel-Rivals-Analyser.git


Start and Initialise Virtual Environment:

  python3 -m venv venv

  source venv/bin/activate

  pip install -r requirements.txt

  set the SECRET_KEY environment variable using:

  LINUX:       export SECRET_KEY='write-your-secret-here' 
  WINDOWS:     $env:SECRET_KEY = 'write-your-secret-here'



```

# Running

```
Set up steps are completed as above (db is created and are in venv).

From main directory:

  flask run

Can now access site on http://127.0.0.1:5000

All users's passwords are "security" (ignore quotes) 
```

# Testing

```
Start and Initialise Virtual Environment:
  
  python3 -m venv env

  source env/bin/activate

  pip install -r requirements.txt

reset database and run the tesing:

  pytest test/unitTests.py

  test/izzy_test.py
