from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.get("/")
def index():
    # args = request.args
    # sitekey = args.get('sitekey')
    widget_mode="managed"
    return render_template("index.html", sitekey=os.getenv("TUNSTILE_MANAGED_SITE_KEY"), widget_mode=widget_mode, nav_classes=_nav_classes(widget_mode))

@app.get("/invisible")
def invisible():
    widget_mode="invisible"
    return render_template("index.html", sitekey=os.getenv("TUNSTILE_INVISIBLE_SITE_KEY"), widget_mode=widget_mode, nav_classes=_nav_classes(widget_mode))

@app.post("/check-challenge")
def check_challenge():
    data = request.get_json(force=True)
    token = data["token"]
    widget_mode = data["widget_mode"]
    secret_key = data.get("secret_key", None)

    return _check_challenge(token=token, widget_mode=widget_mode, secret_key=secret_key)

def _check_challenge(token, widget_mode, secret_key):
    secret = os.getenv("TUNSTILE_MANAGED_SECRET_KEY")

    if widget_mode == "invisible":
        secret = os.getenv("TUNSTILE_INVISIBLE_SECRET_KEY")

    if secret_key:
        secret = secret_key

    r = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data={"secret": secret, "response": token})
    return r.json()

def _nav_classes(widget_mode):
    classes = ["nav-link active", "nav-link"]

    if widget_mode == "invisible":
        classes = reversed(classes)

    return list(classes)
