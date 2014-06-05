import json
from flask import Flask, redirect, session, url_for, request, flash, render_template
from flask_oauth import OAuth
from flask.ext.mongoengine import MongoEngine
from pymongo import MongoClient
from config import *

with open('config.json', 'r') as f:
    config = json.loads(f.read())

client = MongoClient()
msettings = config['MONGODB']
db = client[config['MONGODB']['DB']]
db.authenticate(msettings['USERNAME'], msettings['PASSWORD'])

oauth = OAuth()
twitter = oauth.remote_app('twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key= config['TWITTER']['CONSUMER_KEY'],
            consumer_secret= config['TWITTER']['CONSUMER_SECRET']
            )


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = MONGODB_SETTINGS
app.config["SECRET_KEY"] = SECRET_KEY
#app.config['SERVER_NAME'] = "http://demos.gsi.dit.upm.es/etsitwitter"

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    if session.has_key('twitter_token'):
        del session['twitter_token']
    return twitter.authorize(callback='http://demos.gsi.dit.upm.es/etsitwitter/oauth-authorized')
#                                next=request.args.get('next') or request.referrer or None))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = '/etsitwitter/thanks'
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    token = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    user = resp['screen_name']
    session['twitter_token'] = token
    session['twitter_user'] = user
    db["credentials"].update({"user": user }, {"user": user, "token": token}, True)
    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/')
def index():
#    return 'Please <a href="./login">LOG IN</a> to help with my research :)'
    return render_template('home.html')

@app.route('/hall')
def hall():
    names = [c["user"] for c in db["credentials"].find()]
    return render_template('thanks.html', names=names)


if __name__ == '__main__':
    app.run()