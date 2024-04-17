from flask import Flask, url_for, session, request, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pandas as pd
import time


# App config
app = Flask(__name__)

app.secret_key = 'fgsdfgarsdk'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

@app.route('/')
def login(): # This will automatically log the user into spotify 
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorizePage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('getTracks', _external=True ))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/getTracks')
def getTracks(): # This will fetch all the songs from my spotify account
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items'] 
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]
        if (len(curGroup) < 50):
            break

    df = pd.DataFrame(results, columns=["song names"]) 
    df.to_csv('songs.csv', index=False)
    return "done"

   
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid
    
    # Checking if token is valid
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))
    
    token_valid = True
    return token_info, token_valid

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="f8d23fae02c54efc8cdd63eff3f44da4",
        client_secret="ea7f811e3a28423da5b315fe5284dd29",
        redirect_uri=url_for('authorizePage', _external=True ),
        scope="user-library-read"
    )