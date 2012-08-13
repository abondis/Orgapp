import sys
import os
sys.path.extend(['lib'])
from bottle import run, static_file, request
from bottle import view, redirect, template, url
from bottle import post, get
from bottle import app
from tasks import Orgapp
from doc import Doc
from beaker.middleware import SessionMiddleware


t = Orgapp()
d = Doc()
d.cache_all()


@get('/')
def hello():
    return "Hello World!"


@get('/static/<path:path>', name='static')
def static(path):
    return(static_file(path, root="static/"))


def l2w(_d, dico, idx=1):
    """ Converts a list of path, to an entry similar to os.walk"""
    #'/app/config/config-example.ini'
    _p = os.path.split(_d)
    #[ /app/config, config-example.ini ]
    dico[_p[0]] = dico.get(_p[0], [set(), set()])
    #{ '/app/config': [ [], [] ] }
    if _p[1] != '':
        dico[_p[0]][idx].add(_p[1])
    _path = os.path.split(_p[0])
    if _path[1] != '':
        dico[_path[0]] = dico.get(_path[0], [set(), set()])
        dico[_path[0]][0].add(_path[1])
        l2w(_path[0], dico, idx=0)


def make_code_menu(pagename=None):
    """gets a list a menus for the wiki pages"""
    menu = []
    if pagename:
        # display details
        pass
    menu.append(
        {'url': url("show_tree"), 'title': "Show tree"})
    menu.append(
        {'url': url('show_commits'), 'title': "Show commits"})
    return(menu)


@get('/code/commits', name='show_commits')
@view('show_list')
def show_commits():
    """Show repo's commits"""
    s = request.environ.get('beaker.session')
    s['branch'] = request.query.branch or s.get('branch', 'HEAD')
    # using walker and a ref (branch)
    w = d.r.get_walker([d.r.refs[s['branch']]])
    #w = r.get_walker([r.refs['refs/heads/sqlite']])
    l = [x.commit for x in w]
    menu = make_code_menu()
    return(
        dict(
            listing=l,
            leftmenu=menu,
            branches=d.r.get_refs(),
            current_branch=s['branch'],
            title="Show commits"))


@get('/code/browse/<path:path>/show', name='display_file')
@view('display_file')
def display_file(path):
    s = request.environ.get('beaker.session')
    s['branch'] = request.query.branch or s.get('branch', 'HEAD')
    # get the tree for the branch
    tree_id = d.r[s['branch']].tree
    # get the objects in this tree
    objects = d.r.object_store.iter_tree_contents(tree_id)
    path_sha = [x.sha for x in objects if x.path == path]
    menu = make_code_menu()
    if len(path_sha) == 1:
        content = d.r.get_object(path_sha[0]).as_raw_string().split('\n')
    else:
        content = ["sorry, could not find this file!"]
    return(
        dict(
            content=content,
            leftmenu=menu,
            branches=d.r.get_refs(),
            current_branch=s['branch'],
            title="Display " + path))


@get('/code/browse', name='show_tree')
@get('/code/browse/', name='show_tree')
@get('/code/browse/<path:path>', name='show_tree')
@view('show_files')
def show_tree(path=''):
    """Show repo's tree"""
    s = request.environ.get('beaker.session')
    s['branch'] = request.query.branch or s.get('branch', 'HEAD')
    # get the tree for the branch
    tree_id = d.r[s['branch']].tree
    # get the objects in this tree
    objects = d.r.object_store.iter_tree_contents(tree_id)
    #get the paths of the objects
    l = [x.path for x in objects]
    dico = {}
    for x in l:
        l2w(x, dico)
    hierarchy = dico[path]
    menu = make_code_menu()
    if path == "":
        current_path = '/code/browse'
    else:
        current_path = '/code/browse/' + path
    return(
        dict(
            current_path=current_path,
            listing=hierarchy,
            leftmenu=menu,
            branches=d.r.get_refs(),
            current_branch=s['branch'],
            title="Show tree"))


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
@view('wiki/list_wiki_pages')
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
@view('wiki/edit_wiki_page')
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
@view('wiki/new_wiki_page')
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
@view('wiki/edit_wiki_page')
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
                'wiki/wiki_page',
                title=path,
                content=content,
                leftmenu=menu))


@get('/tasks', name='tasks')
@view('tasks/list_tasks')
def lsTasks():
    menu = make_tasks_menu()
    return(dict(tasks_list=t.ls(), title="Task list", leftmenu=menu))


@get('/tasks/add', name='add_task')
@view('tasks/tasks_add')
def add_task():
    menu = make_tasks_menu()
    statuses = t.get_statuses()
    return(dict(title="Add task", leftmenu=menu, statuses=statuses))


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
    session_opts = {
            'session.type': 'file',
            'session.cookie_expires': 300,
            'session.data_dir': '/tmp/beaker-session',
            'session.auto': True
    }
    webapp = SessionMiddleware(app(), session_opts)
    run(app=webapp, host='0.0.0.0', port=8080, debug=True, reloader=True)
