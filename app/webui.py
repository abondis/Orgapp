import sys
sys.path.extend(['lib'])
from bottle import route, run, static_file, request
from bottle import view, redirect
from tasks import Orgapp
import doc


t = Orgapp()
@route('/')
def hello():
  return "Hello World!"


@route('/doc/<path>/edit')
@view('edit_wiki_page')
def edit_wiki_page(path):
  content = doc.render("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content))

@route('/doc/<path>/edit', method='POST')
@view('edit_wiki_page')
def save_wiki_page(path):
  content = request.forms.content
  doc.save("../doc/{0}.md".format(path), content)
  doc.commit("doc/{0}.md".format(path))
  doc.cache("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content))

#TODO: cache pages another way, ie: cp -R doc cache + render
@route('/doc/<filename:re:[^\.]*>')
def show_wiki_page(filename):
  return static_file(filename, "../doc/cache") 
  

@route('/doc/<path:path>')
def show_wiki_resources(path):
  return static_file(path, "../doc") 

@route('/tasks')
@view('tasks')
def lsTasks():
  return(dict(tasks=t.ls()))

@route('/tasks/add')
@view('tasks_add')
def add_task():
  return(dict())

@route('/tasks/add', method='POST')
def receive_new_task():
  name = request.forms.name
  position = request.forms.position
  status = request.forms.status
  t.add(name, position, status)
  redirect('/tasks')

if __name__ == '__main__':
  run(host='localhost', port=8080, debug=True, reloader=True)
