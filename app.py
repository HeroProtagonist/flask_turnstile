from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template("index.html", sitekey=os.getenv("TURNSTILE_SITE_KEY"))

@app.post("/check-challenge")
def check_challenge():
    breakpoint()
    data = request.get_json(force=True)

    return _check_challenge(data["token"])

def _check_challenge(token):
     r = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data={"secret": os.getenv("TUNSTILE_SECRET_KEY"), "response": token})
     return r.json()
