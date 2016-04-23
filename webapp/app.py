from flask      import *
from json       import dumps

from currentMatchPredict import getCurrentMatch

def reprS(x):
    return repr(str(x))

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'I9pXgEj80UXru'
app.jinja_env.globals.update(repr=reprS)

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
    print('meh..')
    return dumps(getCurrentMatch(name, region))

app.run( \
    host=app.config['HOST'],
    port=app.config['PORT'],
    threaded=True,
    debug=True
    )
