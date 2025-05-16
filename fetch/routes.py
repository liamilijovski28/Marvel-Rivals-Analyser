from fetch import db
import requests
from fetch.controllers import try_change_settings, try_login, try_signup
from flask import jsonify, session, render_template, redirect, url_for, flash
from fetch.forms import LoginForm, SignupForm, SettingsForm
from werkzeug.security import check_password_hash, generate_password_hash  # Import password hash checker
from fetch.models import RestrictedFriends, Stats, User  # Import your User model
from flask_login import login_required, current_user, login_user, logout_user
from fetch.models import User, FriendRequest
from flask import request
from fetch.blueprints import blueprint

@blueprint.route('/home')
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


@blueprint.route('/heroes')
@login_required
def heroes():
    from flask import request

    player_id = current_user.get_id()
    selected_season = request.args.get("season", "")
    mode = request.args.get("mode", "all").lower()

    if not player_id:
        flash("You must be logged in to view your hero stats.", "danger")
        return redirect(url_for('main.login'))

    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    base_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"

    # Support both single and all-season logic
    season_list = ["0", "1", "1.5", "2"] if selected_season == "" else [selected_season]
    api_responses = []

    for season in season_list:
        url = f"{base_url}?season={season}"
        try:
            res = requests.get(url, headers=headers).json()
            api_responses.append(res)
        except Exception as e:
            print(f"Failed to fetch season {season}: {e}")

    def calc_wr(matches, wins):
        return round((wins / matches) * 100, 2) if matches > 0 else 0

    def calc_kd(kills, deaths):
        return round(kills / deaths, 2) if deaths > 0 else kills

    def get_hero_data(response, rank_type):
        key = f"heroes_{rank_type}"
        if key not in response:
            return {}
        return {
            h['hero_name'].title(): {
                "assists": h.get("assists", 0),
                "damage": h.get("damage", 0),
                "damage_blocked": h.get("damage_taken", 0),
                "deaths": h.get("deaths", 0),
                "healing": h.get("heal", 0),
                "kills": h.get("kills", 0),
                "matches": h.get("matches", 0),
                "wins": h.get("wins", 0)
            }
            for h in response[key]
        }

    def merge_hero_dicts(hero_lists):
        merged = {}
        for heroes in hero_lists:
            for name, data in heroes.items():
                if name not in merged:
                    merged[name] = data.copy()
                else:
                    for stat in data:
                        merged[name][stat] += data[stat]
        return merged

    def fill_null_heroes(hero_data, all_heroes, hero_class):
        for name in all_heroes[hero_class]:
            if name.title() not in hero_data:
                hero_data[name.title()] = {k: 0 for k in [
                    "assists", "damage", "damage_blocked", "deaths", "healing",
                    "kills", "matches", "wins"
                ]}
        return hero_data

    all_heroes = {
        "vanguard": ["Captain America", "Doctor Strange", "Emma Frost", "Groot", "Hulk", "Magneto", "Peni Parker", "The Thing", "Thor", "Venom"],
        "strategist": ["Adam Warlock", "Cloak & Dagger", "Invisible Woman", "Jeff the Land Shark", "Loki", "Luna Snow", "Mantis", "Rocket Raccoon"],
        "duelist": ["Black Panther", "Black Widow", "Hawkeye", "Hela", "Human Torch", "Iron Fist", "Iron Man", "Magik", "Mister Fantastic", "Moon Knight", "Namor", "Psylocke", "Scarlet Witch", "Spider-man", "Squirrel Girl", "Star-Lord", "Storm", "The Punisher", "Winter Soldier", "Wolverine"]
    }

    # Build ranked/unranked/all hero dicts across all seasons
    ranked_hero_lists = [get_hero_data(res, "ranked") for res in api_responses]
    unranked_hero_lists = [get_hero_data(res, "unranked") for res in api_responses]

    ranked = merge_hero_dicts(ranked_hero_lists)
    unranked = merge_hero_dicts(unranked_hero_lists)

    for group in all_heroes:
        ranked = fill_null_heroes(ranked, all_heroes, group)
        unranked = fill_null_heroes(unranked, all_heroes, group)

    # Combine selected mode
    hero_agg = {}
    for hero in ranked:
        r = ranked[hero]
        u = unranked[hero]
        combine = lambda stat: (r[stat] + u[stat]) if mode == "all" else (r[stat] if mode == "ranked" else u[stat])
        matches = combine("matches")
        wins = combine("wins")
        deaths = combine("deaths")
        kills = combine("kills")
        hero_agg[hero] = {
            "assists": round(combine("assists"), 2),
            "damage": round(combine("damage"), 2),
            "damage_blocked": round(combine("damage_blocked"), 2),
            "deaths": deaths,
            "healing": round(combine("healing"), 2),
            "kills": kills,
            "matches": matches,
            "wins": wins,
            "losses": matches - wins,
            "win_rate": calc_wr(matches, wins),
            "kd": calc_kd(kills, deaths)
        }

    return render_template('Heroes.html', title='Heroes', heroes=hero_agg, all_heroes=all_heroes)

@blueprint.route('/matches')
@login_required
def matches():
    player_id = current_user.get_id()

    if not player_id:
        flash("You must be logged in to view your match stats.", "danger")
        return redirect(url_for('main.login'))

    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    response = requests.get(url, headers=headers).json()

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

@blueprint.route('/api/player/<player_id>/matches')
def player_matches(player_id):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}/match-history"
    response = requests.get(url, headers=headers)

    return jsonify(response.json())


@blueprint.route('/api/heroes')
def get_heroes():
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = "https://marvelrivalsapi.com/api/v1/heroes"
    response = requests.get(url, headers=headers)

    return jsonify(response.json())


@blueprint.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    user = current_user

    # --- Handle sending friend request ---
    if request.method == "POST":
        search_username = request.form.get("search_username", "").strip()
        if search_username == user.username:
            flash("You can't add yourself as a friend.", "warning")
        else:
            recipient = User.query.filter_by(username=search_username).first()
            if not recipient:
                flash("User not found.", "danger")
            else:
                existing = FriendRequest.query.filter_by(sender_id=user.username, receiver_id=recipient.username).first()
                reverse = FriendRequest.query.filter_by(sender_id=recipient.username, receiver_id=user.username).first()
                if existing or reverse:
                    flash("Friend request already exists or is pending.", "info")
                else:
                    db.session.add(FriendRequest(sender_id=user.username, receiver_id=recipient.username))
                    db.session.commit()
                    flash("Friend request sent!", "success")

    # --- Show accepted friends ---
    accepted = FriendRequest.query.filter(
        ((FriendRequest.sender_id == user.username) | (FriendRequest.receiver_id == user.username)) &
        (FriendRequest.status == 'accepted')
    ).all()

    # --- Show incoming requests ---
    incoming = FriendRequest.query.filter_by(receiver_id=user.username, status='pending').all()

    return render_template("Friends.html", accepted=accepted, incoming=incoming)

@blueprint.route("/compare")
@login_required
def compare():
    return render_template("compare.html")

@blueprint.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if form.submit.data:
               
            new_user, rf = try_change_settings(
                new_username=form.username.data,
                new_password=form.password.data,
                new_playerID=form.player_id.data,
                data_sharing=form.data_sharing.data,
                restricted_friends=form.restricted_friends.data,
                user=current_user
            )
            if new_user.username != current_user.username or new_user.player_id != current_user.player_id or new_user.password != current_user.password:
                logout_user()

        #if logout of close account was pressed
        if form.logout.data:
            logout_user()
            flash("You have been logged out.", "success")
            return redirect(url_for('main.login'))
        if form.close_account.data:
            user = current_user
            db.session.delete(user)
            db.session.commit()
            flash("Your account has been closed.", "success")
            return redirect(url_for('main.signup'))
        if not form.logout.data and not form.close_account.data:
            # If neither logout nor close account was pressed
            flash("Settings updated successfully!", "success")
        return redirect(url_for('main.settings'))
    return render_template("settings.html", form=form)

@blueprint.route('/')
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = try_login(form.username.data, form.password.data)
        if isinstance(result, User):
            login_user(result)
            return redirect(url_for('main.home'))
        else:
            flash(result, 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)


@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        new_user = try_signup(form.username.data, form.password.data, form.player_id.data)
        if isinstance(new_user, User):
            login_user(new_user)
        else:
            flash(new_user, 'danger')
            return redirect(url_for('main.signup'))
        return redirect(url_for('main.home'))
    
    return render_template("signup.html", form=form)

@blueprint.route("/respond_request/<int:req_id>/<action>", methods=["POST"])
@login_required
def respond_request(req_id, action):
    req = FriendRequest.query.get_or_404(req_id)

    if req.receiver_id != current_user.username:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("main.friends"))

    sender = User.query.filter_by(username=req.sender_id).first()
    receiver = User.query.filter_by(username=req.receiver_id).first()

    if not sender or not receiver:
        flash("User not found.", "danger")
        return redirect(url_for("main.friends"))

    if action == "accept":
        req.status = "accepted"

        # Add each other as friends (if not already)
        if receiver not in sender.friends:
            sender.friends.append(receiver)
        if sender not in receiver.friends:
            receiver.friends.append(sender)

        flash(f"You are now friends with {sender.username}.", "success")

    elif action == "reject":
        req.status = "rejected"
        flash("Friend request rejected.", "info")

    db.session.commit()
    return redirect(url_for("main.friends"))


@blueprint.route("/remove_friend/<username>", methods=["POST"])
@login_required
def remove_friend(username):
    print(f"Trying to remove: {username}")
    user = current_user
    friend = User.query.filter_by(username=username).first()

    print(f"Current user: {user.username}")
    print(f"User's friends: {[f.username for f in user.friends]}")
    print(f"Friend to remove: {friend.username if friend else 'None'}")

    if not friend:
        flash("Friend not found.", "danger")
        return redirect(url_for("main.friends"))

    # Remove the friend both ways
    if friend in user.friends:
        user.friends.remove(friend)
    if user in friend.friends:
        friend.friends.remove(user)

    # ✅ Remove the accepted FriendRequest record from the database
    fr = FriendRequest.query.filter(
        ((FriendRequest.sender_id == user.username) & (FriendRequest.receiver_id == friend.username)) |
        ((FriendRequest.sender_id == friend.username) & (FriendRequest.receiver_id == user.username)),
        FriendRequest.status == 'accepted'
    ).first()

    if fr:
        print(f"Deleting FriendRequest with ID: {fr.id}")
        db.session.delete(fr)

    print(f"User's friends after removal: {[f.username for f in user.friends]}")
    print(f"{friend.username}'s friends after removal: {[f.username for f in friend.friends]}")

    db.session.commit()
    flash(f"Removed {username} from your friends list.", "success")
    return redirect(url_for("main.friends"))
