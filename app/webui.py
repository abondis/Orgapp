import sys
import os
sys.path.extend(['lib'])
from bottle import route, run, static_file, request
from bottle import view, redirect, template, url
from tasks import Orgapp
import doc


t = Orgapp()
@route('/')
def hello():
  return "Hello World!"

#maybe not needed
@route('/tasks/<tid>/update', method='GET')
def update_task(tid):
  """Update task position and status"""
  new_pos = request.query.new_pos
  if new_pos:
    t.move(tid, new_pos)
  new_status = request.query.new_status
  if new_status:
    t.status(tid, new_status)
  

@route('/static/<path:path>', name='static')
def static(path):
  return(static_file(path, root="static/"))

def make_wiki_menu(pagename=None):
  """gets a list a menus for the wiki pages"""
  menu = []
  if pagename:
    menu.append(
      {'url': url("edit_wiki_page", path=pagename),
        'title': "Edit "+pagename})
    menu.append(
      {'url': url("show_wiki_page", path=pagename),
        'title': pagename})
  menu.append(
    {'url': url("list_wiki_pages"), 'title': "List wiki pages"})
  menu.append(
    {'url': "#", 'title': "Create a new page"})
  return(menu)

@route('/doc', name="doc_index")
def doc_index():
  if os.path.exists("../doc/cache/Index"):
    return(show_wiki_page('Index'))
  else:
    return(list_wiki_pages())
    

@route('/doc/List', name="list_wiki_pages")
@view('list_wiki_pages')
def list_wiki_pages():
  pages_list = doc.list_pages("../doc/*.*")
  pages_dict = [ {'url': url("show_wiki_page", path=x), 'title':x} for x in pages_list ]
  menu = make_wiki_menu()
  return(
    dict(
      title="Wiki pages",
      pages_list=pages_dict,
      leftmenu=menu))

@route('/doc/<path>/edit', name="edit_wiki_page")
@view('edit_wiki_page')
def edit_wiki_page(path):
  menu = make_wiki_menu(path)
  content = doc.render("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(
    dict(
      pagename=pagename,
      content=content,
      title="Edit {0}".format(path),
      leftmenu=menu))

@route('/doc/<path>/edit', method='POST')
@view('edit_wiki_page')
def save_wiki_page(path):
  menu = make_wiki_menu(path)
  content = request.forms.content
  doc.save("../doc/{0}.md".format(path), content)
  doc.commit("doc/{0}.md".format(path))
  doc.cache("../doc/{0}.md".format(path))
  pagename = '/doc/'+path
  return(
    dict(
      pagename=pagename,
      content=content,
      title="Edit {0}".format(path),
      leftmenu=menu))

@route('/doc/<path>', name="show_wiki_page")
def show_wiki_page(path):
  # if the file exists in doc and cache, serve it raw
  if os.path.exists('../doc/{0}'.format(path)):
    return(static_file(path, root='../doc/'))
  #else this is a rendered document
  else: 
    with open('../doc/cache/{0}'.format(path)) as _f:
      content = _f.read()
    menu = make_wiki_menu(path)
    return(template('wiki_page', title=path, content=content, leftmenu=menu))

@route('/tasks', name='tasks')
@view('tasks')
def lsTasks():
  return(dict(tasks_list=t.ls(), title="Task list"))

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
  run(host='0.0.0.0', port=8080, debug=True, reloader=True)
