from flask import render_template
from fetch import app
import requests
from flask import jsonify
from fetch.forms import LoginForm, SignupForm
from flask import render_template, redirect, url_for, flash



@app.route('/home')
def home():
    player_id = "813581637"
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    update_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}/update"

    update_response = requests.get(update_url, headers=headers)


    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"

    response = ( requests.get(url, headers=headers) ).json()

    kill_total = response['overall_stats']['unranked']['total_kills'] + response['overall_stats']['ranked']['total_kills']
    death_total = response['overall_stats']['unranked']['total_deaths'] + response['overall_stats']['ranked']['total_deaths']
  

    player = {"matches" : response['overall_stats']['total_matches'], "wins" : response['overall_stats']['total_wins'], 
    "losses" : (response['overall_stats']['total_matches'] - response['overall_stats']['total_wins']), 
    "kd" : round( (kill_total / death_total), 2), 
    "win_rate" : round( (( response['overall_stats']['total_wins'] / response['overall_stats']['total_matches'] ) * 100), 2) }
    
    
    return render_template('home page.html', title = 'Home', player = player)

@app.route('/heroes')
def heroes():
    player_id = "813581637"

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    response = ( requests.get(url, headers=headers) ).json()

    def calc_wr(matches, wins):
        if matches == 0:
            return 0
        else:
            return round(((wins / matches)*100), 2)
        
    def calc_kd(kills, deaths):
        if deaths == 0:
            return kills #technically undefined, but this an approachable simplification for the user
        else:
            return round((kills / deaths), 2)



    def get_hero_data(response, rank_type):#rank type is either "ranked" or "unranked"
        heroes = {}
        index = 0
        items = len(response["heroes_" + rank_type]) 
        while index < (items):#loops through hero data returned from the request, storing all stats in a dict nested in a dict
            current_hero = response["heroes_" + rank_type][index]
            heroes[current_hero['hero_name'].title()] = {"assists":current_hero["assists"], "damage":current_hero["damage"], 
            "damage_blocked":current_hero["damage_taken"], "deaths": current_hero["deaths"], "healing":current_hero["heal"], 
            "kills":current_hero["kills"], "matches":current_hero["matches"], "wins":current_hero["wins"]}
            index = index + 1
        return heroes
    
    def fill_null_heroes(hero_data, all_heroes, hero_class):#adds all heroes that there is no data for in a set of hero data (automatically 0 in all stats)
        for foo in all_heroes[hero_class]:
            if (foo in hero_data) == False:
                hero_data[foo.title()] = {"assists":0,"damage":0,"damage_blocked":0,"deaths":0,"healing":0,
                "kills":0,"matches":0,"wins":0}
        return hero_data

    ranked_heroes = get_hero_data(response, "ranked")
    unranked_heroes = get_hero_data(response, "unranked")

    all_heroes = {"vanguard": ["Captain America", "Doctor Strange", "Emma Frost", "Groot", "Hulk", "Magneto", "Peni Parker", 
    "The Thing", "Thor", "Venom"], "strategist" : ["Adam Warlock", 
    "Cloak & Dagger", "Invisible Woman", "Jeff the Land Shark", "Loki", "Luna Snow", 
    "Mantis", "Rocket Raccoon"], "duelist" : ["Black Panther", "Black Widow", "Hawkeye", "Hela", "Human Torch", 
    "Iron Fist", "Iron Man", "Magik",
    "Mister Fantastic", "Moon Knight", "Namor", "Psylocke", "Scarlet Witch", "Spiderman", "Squirrel Girl", "Star-Lord",
    "Storm", "The Punisher", "Winter Soldier", "Wolverine"]}

    for h_class in ["vanguard", "strategist", "duelist"]:
        ranked_heroes = fill_null_heroes(ranked_heroes.copy(), all_heroes, h_class)
        unranked_heroes = fill_null_heroes(unranked_heroes.copy(), all_heroes, h_class)

    hero_agg = {} #aggregate hero data
    for hero in ranked_heroes:
        rHero = ranked_heroes[hero]
        uHero = unranked_heroes[hero]
        hero_agg[hero] = { "assists":round((rHero["assists"] + uHero["assists"]),2), 
        "damage_blocked":round((rHero["damage_blocked"] + uHero["damage_blocked"]),2), "damage":round((rHero["damage"] + uHero["damage"]),2),   
        "deaths":(rHero["deaths"] + uHero["deaths"]), "kills":(rHero["kills"] + uHero["kills"]), 
        "healing":round((rHero["healing"] + uHero["healing"]),2), "matches":(rHero["matches"] + uHero["matches"]),
        "wins":(rHero["wins"] + uHero["wins"]), "losses":((rHero["matches"] + uHero["matches"]) - (rHero["wins"] + uHero["wins"])),
        "win_rate":calc_wr((rHero["matches"] + uHero["matches"]), (rHero["wins"] + uHero["wins"])), 
        "kd":calc_kd((rHero["kills"] + uHero["kills"]), (rHero["deaths"] + uHero["deaths"]))}

 

    return render_template('Heroes.html', title = 'Heroes', heroes = hero_agg, all_heroes = all_heroes)

@app.route('/matches')
def matches():
    player_id = "813581637"
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    response = requests.get(url, headers=headers).json()

    print("== Player Profile Response ==")
    print(response)


    display_name = response.get("name", "Unknown")
    ranked = response['overall_stats']['ranked']
    unranked = response['overall_stats']['unranked']

    kills = ranked['total_kills'] + unranked['total_kills']
    deaths = ranked['total_deaths'] + unranked['total_deaths']
    matches_played = response['overall_stats']['total_matches']
    wins = response['overall_stats']['total_wins']

    stats = {
        "kd": round(kills / deaths, 2) if deaths > 0 else kills,
        "matches": matches_played,
        "wins": wins,
        "losses": matches_played - wins,
        "win_rate": round((wins / matches_played) * 100, 2) if matches_played > 0 else 0
    }


    return render_template("matches.html", username=player_id, display_name=display_name, stats=stats)

@app.route('/api/player/<player_id>/matches')
def player_matches(player_id):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}/match-history"
    response = requests.get(url, headers=headers)

    return jsonify(response.json())


@app.route('/api/heroes')
def get_heroes():
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = "https://marvelrivalsapi.com/api/v1/heroes"
    response = requests.get(url, headers=headers)

    return jsonify(response.json())


@app.route("/friends")
def friends():
    return render_template("Friends.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Add your login logic here
        username = form.username.data
        password = form.password.data
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home')) 
    return render_template('login.html', form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Add your user creation logic here
        flash("Account created successfully!", "success")
        return redirect(url_for('home'))
    return render_template("signup.html", form=form)