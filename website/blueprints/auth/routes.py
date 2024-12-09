import requests
from flask import redirect, url_for, request, flash
from flask_login import login_user, logout_user
from requests.exceptions import HTTPError

from blueprints.auth import bp
from config import Config
from utils import User

DISCORD_AUTH_URL = f"{Config.DISCORD_API_BASE_URL}/oauth2/authorize"
DISCORD_TOKEN_URL = f"{Config.DISCORD_API_BASE_URL}/oauth2/token"
DISCORD_USER_URL = f"{Config.DISCORD_API_BASE_URL}/users/@me"


@bp.route("/login")
def login():
    params = {
        "client_id": Config.DISCORD_CLIENT_ID,
        "redirect_uri": Config.DISCORD_REDIRECT_URI,
        "response_type": "code",
        "scope": "identify email",
    }
    discord_login_url = f"{DISCORD_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(discord_login_url)


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed!", 400

    data = {
        "client_id": Config.DISCORD_CLIENT_ID,
        "client_secret": Config.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.DISCORD_REDIRECT_URI,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        # Exchange code for access token
        response = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        token = response.json()
        access_token = token["access_token"]

        # Fetch user info
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_response = requests.get(DISCORD_USER_URL, headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()

        # Create a User object
        user = User.query.filter_by(discord_id=user_data["id"]).first()
        if user is None:
            flash("You must join the discord")
            return redirect(url_for("main.index"))
        # Log the user in with Flask-Login
        login_user(user)

        # Redirect to the main page or dashboard
        return redirect(url_for("main.index"))

    except HTTPError as http_err:
        return f"HTTP error occurred: {http_err}", 500
    except Exception as err:
        return f"Error occurred: {err}", 500


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.index'))
