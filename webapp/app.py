from flask      import *
from time       import sleep
from json       import dumps
from random     import randint

#from DataMiningLoL.currentMatchPredict  import getCurrentMatch

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'I9pXgEj80UXru'
app.jinja_env.globals.update(repr=repr)

@app.route('/')
def page1():
    return render_template('page1.html')

@app.route('/search')
def page2():
    if 'region' not in request.args:
        return "Region can't be empty"
    if 'name' not in request.args:
        return "Name can't be empty"
    region = request.args['region']
    name = request.args['name']
    return render_template('page2.html', region=region, name=name)

@app.route('/data/<region>/<name>')
def data(region, name):
    #sleep(2 * 60)
    return dumps({"matchData": {"winPercent": "51", "playerData": {"redMid": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "redADC": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "blueTop": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "redTop": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "blueADC": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "redJung": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "blueJung": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "redSup": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "blueSup": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}, "blueMid": {"deaths": "4", "assists": "5", "cs": "8", "rank": "rank", "gold": "100", "kills": "3", "summoner": "summoner", "wards": "12", "champion": "Ahri"}}, "winner": "winner"}})
    #return dumps(getCurrentMatch(name, region))

app.run( \
    host=app.config['HOST'],
    port=app.config['PORT'],
    threaded=True,
    debug=True
    )
