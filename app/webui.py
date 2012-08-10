import sys
import os
sys.path.extend(['lib'])
from bottle import run, static_file, request
from bottle import view, redirect, template, url
from bottle import post, get
from tasks import Orgapp
from doc import Doc


t = Orgapp()
d = Doc()


@get('/')
def hello():
    return "Hello World!"


@get('/static/<path:path>', name='static')
def static(path):
    return(static_file(path, root="static/"))


@get('/code', name='code')
@view('show_tree')
def show_tree():
    """Show repo's tree"""
    tree = d.r.open_index()
    return(dict(tree=tree))


def make_wiki_menu(pagename=None):
    """gets a list a menus for the wiki pages"""
    menu = []
    if pagename:
        menu.append(
            {'url': url("edit_wiki_page", path=pagename),
             'title': "Edit " + pagename})
        menu.append(
            {'url': url("show_wiki_page", path=pagename),
             'title': pagename})
    menu.append(
        {'url': url("list_wiki_pages"), 'title': "List wiki pages"})
    menu.append(
        {'url': url('new_wiki_page'), 'title': "Create a new page"})
    return(menu)


def make_tasks_menu():
    """menus for tasks"""
    menu = []
    menu.append(
        {'url': url("add_task"), 'title': "Add tasks"})
    return(menu)


@get('/doc', name="doc_index")
def doc_index():
    if os.path.exists(d.cache_path + "/Index"):
        return(show_wiki_page('Index'))
    else:
        return(list_wiki_pages())


@get('/doc/List', name="list_wiki_pages")
@view('list_wiki_pages')
def list_wiki_pages():
    pages_list = d.list_pages()
    pages_dict = [
        {'url': url("show_wiki_page", path=x), 'title':x} for x in pages_list]
    menu = make_wiki_menu()
    return(
        dict(
            title="Wiki pages",
            pages_list=pages_dict,
            leftmenu=menu))


@get('/doc/<path>/edit', name="edit_wiki_page")
@view('edit_wiki_page')
def edit_wiki_page(path):
    menu = make_wiki_menu(path)
    content = d.render("{0}.md".format(path))
    pagename = '/doc/' + path
    return(
        dict(
            pagename=pagename,
            content=content,
            title="Edit {0}".format(path),
            leftmenu=menu))


@get('/doc/new', name="new_wiki_page")
@view('new_wiki_page')
def new_wiki_page():
    menu = make_wiki_menu()
    return(
        dict(
            title="New wiki page",
            leftmenu=menu))


@post('/doc/new')
def save_new_wiki_page():
    content = request.forms.content
    pagename = request.forms.pagename
    d.save("{0}.md".format(pagename), content)
    d.commit("{0}.md".format(pagename))
    d.cache("{0}.md".format(pagename))
    pagename = '/doc/' + pagename
    redirect(pagename + "/edit")


@post('/doc/<path>/edit')
@view('edit_wiki_page')
def save_wiki_page(path):
    menu = make_wiki_menu(path)
    content = request.forms.content
    d.save("{0}.md".format(path), content)
    d.commit("{0}.md".format(path))
    d.cache("{0}.md".format(path))
    pagename = '/doc/' + path
    return(
        dict(
            pagename=pagename,
            content=content,
            title="Edit {0}".format(path),
            leftmenu=menu))


@get('/doc/<path>', name="show_wiki_page")
def show_wiki_page(path):
    # if the file exists in doc and cache, serve it raw
    if os.path.exists('{0}/{1}'.format(d.doc, path)):
        return(static_file(path, root=d.doc))
    #else this is a rendered document
    else:
        with open('{0}/{1}'.format(d.cache_path, path)) as _f:
            content = _f.read()
        menu = make_wiki_menu(path)
        return(
            template(
                'wiki_page',
                title=path,
                content=content,
                leftmenu=menu))


@get('/tasks', name='tasks')
@view('tasks')
def lsTasks():
    menu = make_tasks_menu()
    return(dict(tasks_list=t.ls(), title="Task list", leftmenu=menu))


@get('/tasks/add', name='add_task')
@view('tasks_add')
def add_task():
    return(dict(title="Add task"))


@post('/tasks/add')
def receive_new_task():
    name = request.forms.name
    position = request.forms.position
    status = request.forms.status
    t.add(name, position, status)
    redirect('/tasks')


@get('/tasks/<tid>/update')
def update_task(tid):
    """Update task position and status"""
    new_pos = request.query.new_pos
    new_status = request.query.new_status
    t.move(tid, new_pos, new_status)
    if new_status != 'null':
        t.status(tid, new_status)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
