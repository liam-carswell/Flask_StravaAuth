from flask import Flask, redirect, url_for
from flask_dance.contrib.strava import make_strava_blueprint, strava

app = Flask(__name__)

app.secret_key = 'secretkeyhere'
app.config["STRAVA_OAUTH_CLIENT_ID"] = '51104'
app.config["STRAVA_OAUTH_CLIENT_SECRET"] = 'f8fed72df413634c9114b38bf328b20a19d42fd0'


strava_blueprint = make_strava_blueprint(
    scope='activity:read_all,activity:write,profile:read_all', redirect_url="/loggedin")
app.register_blueprint(strava_blueprint)


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
