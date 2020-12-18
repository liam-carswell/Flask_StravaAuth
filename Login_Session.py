import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.strava import make_strava_blueprint, strava

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.config["STRAVA_OAUTH_CLIENT_ID"] = os.environ.get('STRAVA_OAUTH_CLIENT_ID')
app.config["STRAVA_OAUTH_CLIENT_SECRET"] = os.environ.get(
    'STRAVA_OAUTH_CLIENT_SECRET')

strava_blueprint = make_strava_blueprint(
    scope='activity:read_all,activity:write,profile:read_all', redirect_url="/loggedin")
app.register_blueprint(strava_blueprint)

# User goes to homepage, is automatically send to Strava to login. Then redirected to 'redirect_url' above


@app.route("/")
def index():
    if not strava.authorized:
        return redirect(url_for("strava.login"))

    account_info = strava.get("/api/v3/athlete")
    assert account_info.ok
    return account_info.json()


@app.route('/loggedin')
def test():
    return '<h1> You are logged in</h1>'


if __name__ == '__main__':
    app.run(debug=True)
