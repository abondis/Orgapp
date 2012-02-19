#!/usr/bin/env python2
import orgapp
import os
try:
  import io
except:
  import StringIO 
  io = StringIO
try:
  import textile
except Exception:
  pass
from bottle import route, run, static_file, redirect
from bottle import view, template
from bottle import get, post, request, error

@route('/home')
def home():
  return redirect('/')

@route('/')
@view('base')
def home(page='home'):
    return dict(content='<p>Hello, how are you?</p>',
                page=page)

def render_textile(raw):
  return textile.textile(raw)

def wiki_url():
  """
    populates dic path2title and title2path.
    path2title: gives a set (title, titlePath) for every path in the wiki
    title2path: gives a set (fileName, filePath) for every niceURL
  """
  title2path = {}
  path2title = {}
  for i in os.walk('wiki'):
    for j in i[2]:
      filePath = str.strip(i[0]+'/'+j, '\n')
      fileName = str.strip(j, '\n')
      f = open(filePath, 'r')
      title = f.readline()
      titlePath = str.strip(i[0]+'/'+title, '\n')
      f.close
      path2title[filePath] = (title, titlePath)
      title2path[titlePath] = (fileName, filePath)
    # set key for folders
    if len(i[2]):
#      print("i[0]: %s/ i[2]: %s" % (i[0],i[2]))
      foldername = i[0]
      indexpath = i[2][0]
      path2title[foldername+'/'] =  path2title[foldername+'/'+indexpath]
      path2title[foldername] =  path2title[foldername+'/'+indexpath]
      title2path[foldername+'/'] = title2path[path2title[foldername+'/'+indexpath][1]]
      title2path[foldername] = title2path[path2title[foldername+'/'+indexpath][1]]
  return title2path, path2title

@route('/wiki')
@route('/wiki/')
@route('/wiki/:page#.+#')
@view('wiki_2col')
def wiki(page=''):
  # /wiki/machin/blah blah blah
  # -> fullpath = /wiki/machin/blah.txt
  # -> <a href=path2title['fullpath']['1']>title</a>
  print(page)
  page, fullpath = title2path['wiki/%s' % page]
  if os.path.isdir(fullpath):
    files = os.listdir(fullpath)
    dirname = fullpath
  else:
    dirname = os.path.dirname(fullpath)
    files = os.listdir(dirname)

  if not page: page = 'index' 
  print("page: %s, fullpath: %s, dirname: %s" % (page, fullpath, dirname))
  print(static_file(page, root=dirname).output)
  input_str = static_file(page, root=dirname).output.read()
  try:
    import textile
  except Exception:
    input_str = input_str.decode().replace('\n','<br/>')
    return dict(page=page,content=input_str, files=files, path=dirname)
  else:
    return dict(page=page+"_textile",content=render_textile(input_str), files=files, path=dirname, t2p=title2path, p2t=path2title)

@route('/tasks')
@route('/tasks/')
@view('tasks')
def tasks():
  global tasks 
  return dict(tasks=tasks.tasks, page="Tasks List")

@route('/tasks/add')
def addTask():
    return '''<form method="POST" action="/tasks/add">
                <input name="title"     type="text" />
		<input type="submit" />
              </form>'''
  
@post('/tasks/add')
def submitAddTask():
  global tasks 
  title     = request.forms.get('title')
  tasks.addTask(title)
  return redirect('/tasks')

@route('/tasks/move')
def addTask():
    return '''<form method="POST" action="/tasks/move">
                <input name="source"     type="integer" />
                <input name="destination"     type="integer" />
		<input type="submit" />
              </form>'''

@post('/tasks/move')
def moveTask():
  global tasks
  source = int(request.forms.get('source'))
  destination = int(request.forms.get('destination'))
  tasks.moveTask(source, destination)
  return redirect('/tasks')
  #return str(tasks.tasks)

@route('/tasks/context/:id')
def getContext(id):
  tasks.searchByContext(id)

@route('/tasks/:id')
def getTask():
  pass

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'

import bottle
bottle.debug(True)
global title2path
global path2title
#global tasks
tasks = orgapp.taskList('todo.txt')
(title2path, path2title) = wiki_url()
print(path2title.keys())
print(title2path.keys())
#print(path2title['wiki/linux-kernel/imac12.2-arch/linux-imac121.preset'])
run(host='localhost', port=8080,reloader=True)
#run(host='172.16.0.163', port=8080)
