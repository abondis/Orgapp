#!/usr/bin/env python
from bottle import route, run, static_file
from bottle import view, template
from bottle import get, post, request, error

@route('/')
@route('/hello/:name')
def greet(name='Stranger'):
    return 'Hello %s, how are you?' % name

@route('/wiki/:page#.*#')
@view('wiki')
def wiki(page='index'):
  input_str = static_file(page, root='./wiki').output.read().decode().replace('\n','<br/>')
  try:
    import docutils
  except Exception as e:
    return dict(page=page,content=input_str)
  else:
    return dict(page=page+"_docutils",content=input_str)
  return dict(page=page,content=input_str)

@get('/login') # or @route('/login')
def login_form():
    return '''<form method="POST" action="/login">
                <input name="name"     type="text" />
                <input name="password" type="password" />
		<input type="submit" />
              </form>'''

@post('/login') # or @route('/login', method='POST')
def login_submit():
    name     = request.forms.get('name')
    password = request.forms.get('password')
    if name == 'test' and  password == 'test':
        return "<p>Your login was correct</p>"
    else:
        return "<p>Login failed</p>"

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='./static')

@error(404)
def error404(error):
    return 'you might be looking for something you won\'t get'


run(host='localhost', port=8080)
