import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.strava import make_strava_blueprint, strava
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

app = Flask(__name__)

app.secret_key = 'secretkeyhere'
app.config["STRAVA_OAUTH_CLIENT_ID"] = '51104'
app.config["STRAVA_OAUTH_CLIENT_SECRET"] = 'f8fed72df413634c9114b38bf328b20a19d42fd0'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


strava_blueprint = make_strava_blueprint(
    scope='activity:read_all,activity:write,profile:read_all', redirect_url="/loggedin")
app.register_blueprint(strava_blueprint)

strava_blueprint.storage = SQLAlchemyStorage(
    OAuth, db.session, user=current_user)


@app.route("/")
def index():
    if not strava.authorized:
        return redirect(url_for("strava.login"))

    account_info = strava.get("/api/v3/athlete")
    assert account_info.ok
    return account_info.json()


@app.route('/loggedin')
@login_required
def test():
    return '<h1> You are logged in</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
