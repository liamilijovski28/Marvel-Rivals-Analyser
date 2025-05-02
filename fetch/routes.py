from flask import render_template
from fetch import app
import requests
import json
@app.route('/')
@app.route('/home')
def home():
    
    
    url = "https://marvelrivalsapi.com/api/v1/player/813581637"
    headers = {
        "x-api-key": "a5cc115f8d7507f2fc5fb842dfb2ee8fe3f263c2f5ab6825dd3f6846e582d84a"
    }

    response = ( requests.get(url, headers=headers) ).json()

    kill_total = response['overall_stats']['unranked']['total_kills'] + response['overall_stats']['ranked']['total_kills']
    death_total = response['overall_stats']['unranked']['total_deaths'] + response['overall_stats']['ranked']['total_deaths']
  

    player = {"matches" : response['overall_stats']['total_matches'], "wins" : response['overall_stats']['total_wins'], 
    "losses" : (response['overall_stats']['total_matches'] - response['overall_stats']['total_wins']), 
    "kd" : round( (kill_total / death_total), 2), 
    "win_rate" : round( (( response['overall_stats']['total_wins'] / response['overall_stats']['total_matches'] ) * 100), 2) }
    
    
    return render_template('home page.html', title = 'Home', player = player)
