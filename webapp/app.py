from flask      import *
from time       import sleep
from json       import dumps
from random     import randint

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
    sleep(2 * 60)
    status = ['win', 'lose', 'oops']
    return dumps({
                'status': status[randint(0, 2)],
                'player_name': name,
                'player_ladder': 'ladder ?!',
                'player_winratio': '%d%%' %randint(0, 100)
                })

app.run( \
    host=app.config['HOST'],
    port=app.config['PORT'],
    threaded=True,
    debug=True
    )
