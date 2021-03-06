import crosswikis as cw
from flask import (Flask, request, session, g, redirect, url_for, abort,
  render_template, flash)

app = Flask(__name__)
app.config.from_object('config')

def isZeroLength(obj):
  """Jinja2 test for zero-length objects."""
  return len(obj) == 0
app.jinja_env.tests['zerolength'] = isZeroLength

@app.route('/')
def index():
  """Index page."""
  return render_template('index.html', title='Justin Huang')

@app.route('/crosswikis', methods=['GET'])
def crosswikis():
  """Crosswikis page. Performs a search if given the arg 'arg', otherwise, just
  shows a search box."""
  if 'arg' in request.args:
    arg = request.args['arg']
    entities = cw.getEntityDistribution(app.config['CROSSWIKIS_DB_PATH'], arg)
    return render_template(
      'crosswikis.html',
      title='Crosswikis lookup',
      scripts=['jquery-1.9.0.min.js', 'crosswikis.js'],
      entities=entities
    )
  else:
    return render_template(
      'crosswikis.html',
      title='Crosswikis lookup',
      scripts=['jqeury-1.9.0.min.js'],
      entities=None
    )

if __name__ == '__main__':
  if app.config['DEBUG']:
    app.run(debug=True)
  else:
    app.run(host='0.0.0.0')
