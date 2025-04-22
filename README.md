# Marvel Rivals Analyser
This project will analyse the gameplay of users, both on a per match, and over career basis. Whilst other stats and trackers apps exist (both in-game & third-party), this project takes a deeper look at the statistics, rather than just providing general win rate information.


# Marvel Rivals Basics
In Rivals, two teams of 6 players battle each other for control of an objective. Each player plays a character which is one of three classes – Duelist, Vanguard, & Strategist. Broadly speaking, Duelists are meant to do damage and defeat opponents, Vanguards are meant to survive taking damage and stop their team from being damaged, Strategists are meant to heal their team and buff them.

Each game a user logs, they will submit the following statistics:

-Game mode (This project will support only either Quick Match or Ranked)

-Current Season (Is either 0, a positive integer, or a positive integer + 0.5)/Alternatively could get user to input current date

-Character (who they played), 

-KOs (How many opponents they helped defeated through damage), Deaths (How many times they were defeated), 

-Assists (How many opponents they helped defeat through buffs), 

-Final Hits (How many opponents they did the final damage to defeat)

-Damage (Damage dealt to opponents)

-Damage Blocked (Damage the user took)

-Healing (Health restored by the user)

-Accuracy (Ratio of hit attacks vs misses)

-Win/Loss (Boolean of whether their team won or lost)

-MVP/SVP (MVP is the “best” on the winning team, SVP is the same but for the losing team)

-KO streak award (If a player gets 3 or more final hits in quick succession, they get a badge for how many they got – 3-6 are tracked as numbers, 7 or more is classed as “Unstoppable!”.)

(And yes KO streak is not a streak of KOs. The game confusingly calls it that for some reason. This is not particularly important however.)


Optional - Limited team stats:

-An entry for each other team member (5 players), containing their class and how many times they died







