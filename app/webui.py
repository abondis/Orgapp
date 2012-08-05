import sys
import os
sys.path.extend(['lib'])
from bottle import route, run, static_file, request
from bottle import view, redirect, template
from tasks import Orgapp
import doc


t = Orgapp()
@route('/')
def hello():
  return "Hello World!"

@route('/static/<path:path>', name='static')
def static(path):
  return(static_file(path, root="static/"))


@route('/doc/<path>/edit')
@view('edit_wiki_page')
def edit_wiki_page(path):
  content = doc.render("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content, title="Edit {0}".format(path)))

@route('/doc/<path>/edit', method='POST')
@view('edit_wiki_page')
def save_wiki_page(path):
  content = request.forms.content
  doc.save("../doc/{0}.md".format(path), content)
  doc.commit("doc/{0}.md".format(path))
  doc.cache("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(dict(pagename=pagename, content=content, title="Edit {0}".format(path)))

@route('/doc/<path>')
def show_wiki_page(path):
  # if the file exists in doc and cache, serve it raw
  if os.path.exists('../doc/{0}'.format(path)):
    return(static_file(path, root='../doc/'))
  #else this is a rendered document
  else: 
    with open('../doc/cache/{0}'.format(path)) as _f:
      content = _f.read()
    return(template('wiki_page', title=path, content=content))

@route('/tasks')
@view('tasks')
def lsTasks():
  return(dict(tasks=t.ls(), title="Task list"))

@route('/tasks/add')
@view('tasks_add')
def add_task():
  return(dict(title="Add task"))

@route('/tasks/add', method='POST')
def receive_new_task():
  name = request.forms.name
  position = request.forms.position
  status = request.forms.status
  t.add(name, position, status)
  redirect('/tasks')

if __name__ == '__main__':
  run(host='localhost', port=8080, debug=True, reloader=True)
