from fetch import db
import requests
from fetch.controllers import try_change_settings, try_login, try_signup
from flask import jsonify, session, render_template, redirect, url_for, flash, request
from fetch.forms import LoginForm, SignupForm, SettingsForm
from werkzeug.security import check_password_hash, generate_password_hash  # Import password hash checker
from fetch.models import RestrictedFriends, Stats, User  # Import your User model
from flask_login import login_required, current_user, login_user, logout_user
from fetch.models import User, FriendRequest
from fetch.blueprints import blueprint
from fetch.forms import SignupForm


def get_role_stats(player_id, season=None):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    season_list = ["0", "1", "1.5", "2"] if not season else [season]
    base_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    role_mapping = {
        "Vanguard": [
            "Captain America", "Doctor Strange", "Emma Frost", "Groot", "Hulk", "Magneto", "Peni Parker", "The Thing", "Thor", "Venom"
        ],
        "Support": [
            "Adam Warlock", "Cloak & Dagger", "Invisible Woman", "Jeff the Land Shark", "Loki", "Luna Snow", "Mantis", "Rocket Raccoon"
        ],
        "Duelist": [
            "Black Panther", "Black Widow", "Hawkeye", "Hela", "Human Torch", "Iron Fist", "Iron Man", "Magik", "Mister Fantastic",
            "Moon Knight", "Namor", "Psylocke", "Scarlet Witch", "Spider-man", "Squirrel Girl", "Star-Lord", "Storm", "The Punisher",
            "Winter Soldier", "Wolverine"
        ]
    }

    role_stats = {role: {"matches": 0, "wins": 0, "kills": 0, "deaths": 0} for role in role_mapping}

    for season_id in season_list:
        url = f"{base_url}?season={season_id}"
        try:
            res = requests.get(url, headers=headers).json()
        except Exception as e:
            print(f"Error fetching role stats for season {season_id}: {e}")
            continue

        for mode in ["ranked", "unranked"]:
            for hero in res.get(f"heroes_{mode}", []):
                hero_name = hero["hero_name"].title()
                for role, heroes in role_mapping.items():
                    if hero_name in heroes:
                        role_stats[role]["matches"] += hero.get("matches", 0)
                        role_stats[role]["wins"] += hero.get("wins", 0)
                        role_stats[role]["kills"] += hero.get("kills", 0)
                        role_stats[role]["deaths"] += hero.get("deaths", 0)

    simplified = {}
    for role, stats in role_stats.items():
        m = stats["matches"]
        w = stats["wins"]
        k = stats["kills"]
        d = stats["deaths"]
        simplified[role] = {
            "Matches": m,
            "WinPct": round((w / m) * 100, 1) if m else 0,
            "KDA": round((k / d), 1) if d else k
        }

    return simplified


def get_simplified_hero_stats(player_id, season=None):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    season_list = ["0", "1", "1.5", "2"] if not season else [season]
    base_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    hero_data = {}

    for s in season_list:
        url = f"{base_url}?season={s}"
        try:
            res = requests.get(url, headers=headers).json()
        except Exception as e:
            print(f"Error fetching hero stats for season {s}: {e}")
            continue

        for mode in ["ranked", "unranked"]:
            for h in res.get(f"heroes_{mode}", []):
                name = h["hero_name"].title()
                if name not in hero_data:
                    hero_data[name] = {
                        "matches": 0, "wins": 0, "kills": 0, "deaths": 0
                    }
                hero_data[name]["matches"] += h.get("matches", 0)
                hero_data[name]["wins"] += h.get("wins", 0)
                hero_data[name]["kills"] += h.get("kills", 0)
                hero_data[name]["deaths"] += h.get("deaths", 0)

    simplified_stats = {}
    for hero, stats in hero_data.items():
        matches = stats["matches"]
        wins = stats["wins"]
        kills = stats["kills"]
        deaths = stats["deaths"]
        win_pct = round((wins / matches) * 100, 1) if matches else 0
        kda = round((kills / deaths), 1) if deaths else kills
        simplified_stats[hero] = {
            "Matches": matches,
            "WinPct": win_pct,
            "KDA": kda
        }

    return simplified_stats


def get_total_hero_stats(player_id, season=None):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    base_url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    season_list = ["0", "1", "1.5", "2"] if not season else [season]
    api_responses = []

    for s in season_list:
        url = f"{base_url}?season={s}"
        try:
            res = requests.get(url, headers=headers).json()
            api_responses.append(res)
        except Exception as e:
            print(f"Hero stat fetch failed for season {s}: {e}")

    def extract_hero_stats(resp, mode):
        key = f"heroes_{mode}"
        return resp.get(key, [])

    damage = healing = blocked = 0
    for res in api_responses:
        for mode in ["ranked", "unranked"]:
            for hero in extract_hero_stats(res, mode):
                damage += hero.get("damage", 0)
                healing += hero.get("heal", 0)
                blocked += hero.get("damage_taken", 0)

    return {
        "damage": round(damage, 2),
        "healing": round(healing, 2),
        "blocked": round(blocked, 2)
    }

def get_overall_stats(player_id, season=None):
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}"
    if season:
        url += f"?season={season}"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # print("== DEBUG Raw overall_stats for", player_id, "==")
        # import pprint
        # # pprint.pprint(data.get("overall_stats", {}))  # 👈 This line
    except Exception as e:
        print(f"Error fetching player data: {e}")
        return {}

    stats = data.get("overall_stats", {})
    ranked = stats.get("ranked", {})
    unranked = stats.get("unranked", {})

    def sum_stat(key):
        return ranked.get(key, 0) + unranked.get(key, 0)

    kills = sum_stat("total_kills")
    deaths = sum_stat("total_deaths")
    assists = sum_stat("total_assists")
    damage = sum_stat("damage")
    healing = sum_stat("heal")
    blocked = sum_stat("damage_taken")  # correct key for blocked


    mvps = sum_stat("total_mvps")
    svps = sum_stat("total_svp")
    max_streak = max(ranked.get("max_kill_streak", 0), unranked.get("max_kill_streak", 0))

    return {
        "kda": round(kills / deaths, 2) if deaths > 0 else kills,
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "damage": damage,
        "healing": healing,
        "blocked": blocked,
        "svps": svps
    }


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
    """
    Thin proxy to Marvel Rivals `match-history` endpoint
    so we can attach our API-key serverside *and* forward
    pagination / filter query-params untouched.
    """
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    # read the same optional params the JS might send
    params = {}
    if (skip   := request.args.get("skip")):       params["skip"]       = skip
    if (season := request.args.get("season")):     params["season"]     = season
    if (gm     := request.args.get("game_mode")):  params["game_mode"]  = gm
    if (ts     := request.args.get("timestamp")):  params["timestamp"]  = ts

    url = f"https://marvelrivalsapi.com/api/v1/player/{player_id}/match-history"
    resp = requests.get(url, headers=headers, params=params)
    return jsonify(resp.json())

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
    from fetch.models import User
    player_id = current_user.get_id()
    season = request.args.get("season")
    friend_username = request.args.get("friend")

    # --- Get own stats ---
    user_stats = get_overall_stats(player_id, season)
    user_hero_totals = get_total_hero_stats(player_id, season)
    user_stats.update(user_hero_totals)
    user_hero_stats = get_simplified_hero_stats(player_id, season)

    # --- Friend stats setup ---
    friend_stats = {}
    friend_hero_stats = {}
    friend_name = None

    if friend_username:
        friend_user = User.query.filter_by(username=friend_username).first()
        if friend_user:
            friend_name = friend_user.username
            friend_stats = get_overall_stats(friend_user.player_id, season)
            friend_hero_totals = get_total_hero_stats(friend_user.player_id, season)
            friend_stats.update(friend_hero_totals)
            friend_hero_stats = get_simplified_hero_stats(friend_user.player_id, season)

    # --- Gather accepted friends ---
    accepted = FriendRequest.query.filter(
        ((FriendRequest.sender_id == current_user.username) | (FriendRequest.receiver_id == current_user.username)) &
        (FriendRequest.status == 'accepted')
    ).all()

    friends = []
    for fr in accepted:
        other_username = fr.sender_id if fr.receiver_id == current_user.username else fr.receiver_id
        friend_obj = User.query.filter_by(username=other_username).first()
        if friend_obj:
            friends.append(friend_obj)

    return render_template(
        "compare.html",
        user_stats=user_stats,
        friend_stats=friend_stats,
        friend_name=friend_name,
        user_hero_stats=user_hero_stats,
        friend_hero_stats=friend_hero_stats,
        friends=friends  # ✅ friend dropdown data
    )


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

    if request.method == "POST":
        print("POST received")

    if form.validate_on_submit():
        new_user = try_signup(form.username.data, form.password.data, form.player_id.data)
        if isinstance(new_user, User):
            login_user(new_user)
            return redirect(url_for('main.home'))
        else:
            # Attach signup-specific error to the username field
            form.username.errors.append(new_user)

    # Always render the form (even with errors) so the page displays them
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

@blueprint.route("/api/friend-request", methods=["POST"])
@login_required
def api_friend_request():
    """
    Handles friend-request submissions coming from the navbar (AJAX).
    Returns JSON so the current page doesn’t redirect.
    """
    search_username = request.form.get("search_username", "").strip()
    if not search_username:
        return jsonify(error="Username required"), 400
    if search_username.lower() == current_user.username.lower():
        return jsonify(error="You can’t add yourself"), 400

    recipient = User.query.filter_by(username=search_username).first()
    if not recipient:
        return jsonify(error="User not found"), 404

    # Prevent duplicates or reverse requests
    existing = FriendRequest.query.filter_by(
        sender_id=current_user.username,
        receiver_id=recipient.username
    ).first()
    reverse = FriendRequest.query.filter_by(
        sender_id=recipient.username,
        receiver_id=current_user.username
    ).first()
    if existing or reverse:
        return jsonify(error="Friend request already exists or is pending"), 409

    db.session.add(FriendRequest(sender_id=current_user.username,
                                 receiver_id=recipient.username))
    db.session.commit()

    return jsonify(status="sent", username=search_username), 200
