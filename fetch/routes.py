from fetch import app, db
import requests
from flask import jsonify, session, render_template, redirect, url_for, flash
from fetch.forms import LoginForm, SignupForm, SettingsForm
from werkzeug.security import check_password_hash, generate_password_hash  # Import password hash checker
from fetch.models import RestrictedFriends, Stats, User  # Import your User model
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/home')
@login_required
def home():
    player_id = current_user.get_id()  # Default to a test player ID if not logged in
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    update_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}/update"
    update_response = requests.get(update_url, headers=headers)

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    response = requests.get(url, headers=headers).json()

    if "error" in response:
        flash(response["error"], "danger")
        return render_template('home page.html', title='Home', player={})

    overall_stats = response.get("overall_stats", {})
    ranked = overall_stats.get("ranked", {})
    unranked = overall_stats.get("unranked", {})

    kill_total = unranked.get("total_kills", 0) + ranked.get("total_kills", 0)
    death_total = unranked.get("total_deaths", 0) + ranked.get("total_deaths", 0)
    matches = overall_stats.get("total_matches", 0)
    wins = overall_stats.get("total_wins", 0)

    player = {
        "matches": matches,
        "wins": wins,
        "losses": matches - wins,
        "kd": round(kill_total / death_total, 2) if death_total > 0 else kill_total,
        "win_rate": round((wins / matches) * 100, 2) if matches > 0 else 0
    }

    players_stats = Stats(player_id=player_id, wins=player['wins'], losses=player['losses'],
                          matches_played=player['matches'], win_rate=player['win_rate'], Kd=player['kd'])

    existing_stats = Stats.query.filter_by(player_id=player_id).first()
    if existing_stats:
        existing_stats.Kd = round(
            (existing_stats.Kd * existing_stats.matches_played + player['kd'] * player['matches']) /
            (existing_stats.matches_played + player['matches']), 2)
        existing_stats.wins += player['wins']
        existing_stats.losses += player['losses']
        existing_stats.matches_played += player['matches']
        existing_stats.win_rate = round(existing_stats.wins / existing_stats.matches_played * 100, 2)
        db.session.add(existing_stats)
    else:
        db.session.add(players_stats)

    db.session.commit()
    return render_template('home page.html', title='Home', player=player)


@app.route('/heroes')
@login_required
def heroes():
    player_id = current_user.get_id()

    if not player_id:
        flash("You must be logged in to view your hero stats.", "danger")
        return redirect(url_for('login'))


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


    def get_hero_data(response, rank_type):
        key = "heroes_" + rank_type
        if key not in response:
            return {}

        heroes = {}
        for current_hero in response[key]:
            heroes[current_hero['hero_name'].title()] = {
                "assists": current_hero.get("assists", 0),
                "damage": current_hero.get("damage", 0),
                "damage_blocked": current_hero.get("damage_taken", 0),
                "deaths": current_hero.get("deaths", 0),
                "healing": current_hero.get("heal", 0),
                "kills": current_hero.get("kills", 0),
                "matches": current_hero.get("matches", 0),
                "wins": current_hero.get("wins", 0)
            }
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
    "Mister Fantastic", "Moon Knight", "Namor", "Psylocke", "Scarlet Witch", "Spider-man", "Squirrel Girl", "Star-Lord",
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
@login_required
def matches():
    player_id = current_user.get_id()

    if not player_id:
        flash("You must be logged in to view your match stats.", "danger")
        return redirect(url_for('login'))

    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    response = requests.get(url, headers=headers).json()

    print("== Player Profile Response ==")
    print(response)

    if "error" in response:
        flash(response["error"], "danger")
        return render_template("matches.html", username=player_id, display_name="Unavailable", stats={})

    display_name = response.get("name", "Unknown")
    overall_stats = response.get("overall_stats", {})
    ranked = overall_stats.get("ranked", {})
    unranked = overall_stats.get("unranked", {})

    kills = ranked.get('total_kills', 0) + unranked.get('total_kills', 0)
    deaths = ranked.get('total_deaths', 0) + unranked.get('total_deaths', 0)
    matches_played = overall_stats.get('total_matches', 0)
    wins = overall_stats.get('total_wins', 0)

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
@login_required
def friends():
    return render_template("Friends.html")

@app.route("/compare")
@login_required
def compare():
    return render_template("compare.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if form.submit.data:
               
            new_username = form.new_username.data
            new_password = form.new_password.data
            new_playerID = form.new_playerID.data.strip()
            data_sharing = form.data_sharing.data == 'yes'
            restricted_friends = form.restricted_friends.data

            user = current_user
            if new_username:
                user.username = new_username
            if new_password:
                user.password = generate_password_hash(new_password)
            if new_playerID:
                user.player_id = new_playerID

            rf = RestrictedFriends.query.filter_by(player_id=user.player_id).first()
            if not rf:
                rf = RestrictedFriends(player_id=user.player_id)
                db.session.add(rf)

            rf.data_sharing = data_sharing
            rf.restricted_friends = restricted_friends

            db.session.commit()
            #updating the login details
            logout_user()
            updated_user = user
            if new_playerID:
                updated_user = User.query.filter_by(player_id=new_playerID).first()
            login_user(updated_user)

        #if logout of close account was pressed
        if form.logout.data:
            logout_user()
            flash("You have been logged out.", "success")
            return redirect(url_for('login'))
        if form.close_account.data:
            user = current_user
            db.session.delete(user)
            db.session.commit()
            flash("Your account has been closed.", "success")
            return redirect(url_for('signup'))
        if not form.logout.data and not form.close_account.data:
            # If neither logout nor close account was pressed
            flash("Settings updated successfully!", "success")
        return redirect(url_for('settings'))
    return render_template("settings.html", form=form)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the username exists in the database
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # If the username exists and the password is correct
            login_user(user)  # Log the user in
            return redirect(url_for('home'))
        else:
            # If the username doesn't exist or the password is incorrect
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login')) 
    return render_template('login.html', form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        player_id = form.player_id.data.strip()
        if not player_id.isdigit() or len(player_id) != 9:
            flash("Player ID must be exactly 9 digits.", "danger")
            return render_template("signup.html", form=form)

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose something else.', 'danger')
            return render_template("signup.html", form=form)
        
        # Check if the playerid already is connected to an account
        existing_player = User.query.filter_by(player_id=player_id).first()
        if existing_player:
            flash("That Player ID is already linked to another account.", "danger")
            return render_template("signup.html", form=form)

        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password)

        # Create a new user with the hashed password and add to the database
        new_user = User(username=username, password=hashed_password, player_id=player_id)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('signup'))
        session['user_id'] = player_id
        return redirect(url_for('home'))
    
    return render_template("signup.html", form=form)
