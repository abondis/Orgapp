from lib.bottle import route, run, static_file
from lib.tasks import Orgapp


t = Orgapp()
@route('/')
def hello():
  return "Hello World!"

@route('/doc/<path:path>')
def show_wiki_page(path):
  return static_file(path, "../doc/cache") 

@route('/tasks')
def lsTasks():
  return(t.ls())


if __name__ == '__main__':
  run(host='localhost', port=8080, debug=True, reloader=True)
