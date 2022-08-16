from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, jsonify, session, render_template
from flask_cors import CORS, cross_origin
from os import environ as env
from urllib.parse import quote_plus, urlencode
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

from auth import requires_auth
CORS(app)

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/callback", methods=["GET"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(env.get("FRONTEND"))

@app.route("/login")
def login_with_redirect():
    return oauth.auth0.authorize_redirect(
        redirect_uri=env.get("BACKEND") + "/callback"
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": env.get("FRONTEND"),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)