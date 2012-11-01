#!/usr/bin/env python
import sys
import os
sys.path.extend(['lib'])
from bottle import run, static_file, request
from bottle import view, redirect, template, url
from bottle import post, get
from bottle import app
#from bottle import mount
from tasks import Orgapp
from doc import Doc
from beaker.middleware import SessionMiddleware
#from mercurial.hgweb import hgweb
import mercurial.commands as hg
from mercurial import ui, localrepo
from dulwich import repo
from cork import Cork
from bottle import SimpleTemplate


t = Orgapp()
d = Doc()
d.cache_all()
hgui = ui.ui()

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('config')
#subproject = hgweb('/tmp/trucmuche')
#mount('/hg/', subproject)

@post('/login')
def login():
    username = request.POST.get('user', '')
    password = request.POST.get('password', '')
    aaa.login(username, password, success_redirect='/', fail_redirect='/truc')

@get('/login', name='login')
def login_get():
    return template('login',
            title='Login')

@get('/logout', name='logout')
def logout():
        aaa.logout(success_redirect='/login')


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


def make_code_menu(project, pagename=None):
    """gets a list a menus for the wiki pages"""
    menu = []
    if pagename:
        # display details
        pass
    menu.append(
        {'url': url("show_tree", project=project), 'title': "Show tree"})
    menu.append(
        {'url': url('show_commits', project=project), 'title': "Show commits"})
    return(menu)


@get('/<project>/code/commits', name='show_commits')
@view('show_list')
def show_commits(project):
    """Show repo's commits"""
    s = request.environ.get('beaker.session')
    if type(d.r[project]) == repo.Repo:
        s['branch'] = request.query.branch or \
            s.get('branch', 'HEAD')
        # using walker and a ref (branch)
        branches = d.r[project].get_refs()
        if s['branch'] in branches:
            w = d.r[project].get_walker([d.r[project].refs[s['branch']]])
            #w = r.get_walker([r.refs['refs/heads/sqlite']])
            l = [x.commit for x in w]
        else:
            l = ["Nothing has yet been done on your repo..."]
    elif type(d.r[project]) == localrepo.localrepository:
        s['branch'] = request.query.branch or \
            s.get('branch', 'default')
        branches = d.r[project].branchmap().keys()
        #if s['branch'] not in branches:
        try:
            hgui.pushbuffer()
            hg.log(hgui, d.r[project], branch=[s['branch']])
            l = hgui.popbuffer().split('\n\n')
        except:
            s['branch'] = 'default'
            l = ["Nothing has yet been done on your repo..."]
    menu = make_code_menu(project)
    return(
        dict(
            listing=l,
            branches=branches,
            leftmenu=menu,
            project=project,
            current_branch=s['branch'],
            title="Show commits"))


@get('/<project>/code/browse/<path:path>/show', name='display_file')
@view('display_file')
def display_file(path, project):
    s = request.environ.get('beaker.session')
    if type(d.r[project]) == repo.Repo:
        s['branch'] = request.query.branch or \
            s.get('branch', 'HEAD')
        # get the tree for the branch
        branches = d.r[project].get_refs()
        tree_id = d.r[project][s['branch']].tree
        # get the objects in this tree
        objects = d.r[project].object_store.iter_tree_contents(tree_id)
        path_sha = [x.sha for x in objects if x.path == path]
        if len(path_sha) == 1:
            content = d.r[project].get_object(path_sha[0]).as_raw_string().split('\n')
        else:
            content = ["sorry, could not find this file!"]
    elif type(d.r[project]) == localrepo.localrepository:
        s['branch'] = request.query.branch or \
            s.get('branch', 'default')
        branches = d.r[project].branchmap().keys()
        if s['branch'] not in branches:
            s['branch'] = d.r[project].branchmap().keys()[0]
        _br = d.r[project][s['branch']]
        hgui.pushbuffer()
        hg.locate(hgui, d.r[project], branch=s['branch'] )
        _file = hgui.popbuffer().split('\n')
        if path in _file:
            content = _br.filectx(path).data().split('\n')
        else:
            content = ["sorry, could not find this file!"]
    menu = make_code_menu(project)
    return(
        dict(
            content=content,
            project=project,
            leftmenu=menu,
            branches=branches,
            current_branch=s['branch'],
            title="Display " + path))


@get('/<project>/code/browse', name='show_tree')
@get('/<project>/code/browse/', name='show_tree')
@get('/<project>/code/browse/<path:path>', name='show_tree')
@view('show_files')
def show_tree(project, path=''):
    """Show repo's tree"""
    if path == "":
        current_path = '/' + project + '/code/browse'
    else:
        current_path = '/' + project + '/code/browse/' + path
    s = request.environ.get('beaker.session')
    l = []
    if type(d.r[project]) == repo.Repo:
        s['branch'] = request.query.branch or \
            s.get('branch', 'HEAD')
        # get the tree for the branch
        branches = d.r[project].get_refs().keys()
        if s['branch'] in branches:
            tree_id = d.r[project][s['branch']].tree
            # get the objects in this tree
            objects = d.r[project].object_store.iter_tree_contents(tree_id)
            #get the paths of the objects
            l = [x.path for x in objects]
        else:
            l = ["Nothing has yet been done on your repo..."]
    elif type(d.r[project]) == localrepo.localrepository:
        s['branch'] = request.query.branch or \
            s.get('branch', 'default')
        branches = d.r[project].branchmap().keys()
        print branches
        #try:
        if s['branch'] not in branches:
            s['branch'] = d.r[project].branchmap().keys()[0]
        hgui.pushbuffer()
        l = hg.locate(hgui, d.r[project], branch=s['branch'] )
        l = hgui.popbuffer().split('\n')
        print l
        #except:
            #s['branch'] = 'default'
            #l = ["Nothing has yet been done on your repo..."]
    dico = {}
    for x in l:
        l2w(x, dico)
    hierarchy = dico[path]
    menu = make_code_menu(project)
    return(
        dict(
            current_path=current_path,
            listing=hierarchy,
            leftmenu=menu,
            branches=branches,
            project=project,
            current_branch=s['branch'],
            title="Show tree"))


def make_wiki_menu(project, pagename=None):
    """gets a list a menus for the wiki pages"""
    menu = []
    if pagename:
        if is_loggued():
            menu.append(
                {'url': url("edit_wiki_page", path=pagename, project=project),
                'title': "Edit " + pagename})
        menu.append(
            {'url': url("show_wiki_page", path=pagename, project=project),
             'title': pagename})
    menu.append(
        {'url': url("list_wiki_pages", project=project), 'title': "List wiki pages"})
    if is_loggued():
        menu.append(
            {'url': url('new_wiki_page', project=project), 'title': "Create a new page"})
    return(menu)


def make_tasks_menu():
    """menus for tasks"""
    menu = []
    if is_loggued():
        menu.append(
            {'url': url("add_task"), 'title': "Add tasks"})
    return(menu)


@get('/<project>/doc', name="doc_index")
def doc_index(project):
    if os.path.exists(d.cache_path + "/" + project +"/Index"):
        return(show_wiki_page('Index', project))
    else:
        return(list_wiki_pages(project))


@get('/<project>/doc/List', name="list_wiki_pages")
@view('wiki/list_wiki_pages')
def list_wiki_pages(project):
    pages_list = d.list_pages(project)
    pages_dict = [
        {'url': url("show_wiki_page", project=project, path=x), 'title':x} for x in pages_list]
    menu = make_wiki_menu(project)
    return(
        dict(
            title="Wiki pages",
            project=project,
            pages_list=pages_dict,
            leftmenu=menu))


@get('/<project>/doc/<path>/edit', name="edit_wiki_page")
@view('wiki/edit_wiki_page')
def edit_wiki_page(project, path):
    aaa.require(role='edit', fail_redirect='/login')
    pagename = '/' + project + '/doc/' + path
    menu = make_wiki_menu(project, path)
    content = d.render("{0}.md".format(path), project)
    return(
        dict(
            pagename=pagename,
            content=content,
            project=project,
            title="Edit {0}".format(path),
            leftmenu=menu))


@get('/<project>/doc/new', name="new_wiki_page")
@view('wiki/new_wiki_page')
def new_wiki_page(project):
    aaa.require(role='edit', fail_redirect='/login')
    menu = make_wiki_menu(project)
    return(
        dict(
            project=project,
            title="New wiki page",
            leftmenu=menu))


@post('/<project>/doc/new')
def save_new_wiki_page(project):
    aaa.require(role='edit', fail_redirect='/login')
    content = request.forms.content
    pagename = request.forms.pagename
    d.save("{0}.md".format(pagename), content, project)
    d.commit("{0}.md".format(pagename), project)
    d.cache("{0}.md".format(pagename), project)
    pagename = '/' + project + '/doc/' + pagename
    redirect(pagename + "/edit")


@post('/<project>/doc/<path>/edit')
@view('wiki/edit_wiki_page')
def save_wiki_page(project, path):
    aaa.require(role='edit', fail_redirect='/login')
    menu = make_wiki_menu(project, path)
    content = request.forms.content
    d.save("{0}.md".format(path), content, project)
    d.commit("{0}.md".format(path), project)
    d.cache("{0}.md".format(path), project)
    pagename = '/' + project + '/doc/' + path
    return(
        dict(
            project=project,
            pagename=pagename,
            content=content,
            title="Edit {0}".format(path),
            leftmenu=menu))


@get('/<project>/doc/<path>', name="show_wiki_page")
def show_wiki_page(path, project):
    # if the file exists in doc and cache, serve it raw
    if os.path.exists('{0}/{1}'.format(d.doc, path)):
        return(static_file(path, root=d.doc))
    #else this is a rendered document
    else:
        with open(d.cache_path + project + '/' + path) as _f:
            content = _f.read()
        menu = make_wiki_menu(project, path)
        return(
            template(
                'wiki/wiki_page',
                project=project,
                title=path,
                content=content,
                leftmenu=menu))


@get('/projects list', name='projects_list')
@view('list_projects')
def projects_list():
    return dict(title='Projects list', listing=d.r.keys())


@get('/tasks', name='tasks')
@get('/')
@view('tasks/list_tasks')
def lsTasks():
    menu = make_tasks_menu()
    return(dict(tasks_list=t.ls(),
        title="Task list",
        leftmenu=menu,
        project=None))


@get('/tasks/add', name='add_task')
@view('tasks/tasks_add')
def add_task():
    aaa.require(role='edit', fail_redirect='/login')
    menu = make_tasks_menu()
    statuses = t.get_statuses()
    return(dict(title="Add task",
        leftmenu=menu,
        project=None,
        statuses=statuses))


@post('/tasks/add')
def receive_new_task():
    aaa.require(role='edit', fail_redirect='/login')
    name = request.forms.name
    position = request.forms.position
    status = request.forms.status
    t.add(name, position, status)
    redirect('/tasks')


@get('/tasks/<tid>/update')
def update_task(tid):
    """Update task position and status"""
    aaa.require(role='edit', fail_redirect='/login')
    new_pos = request.query.new_pos
    new_status = request.query.new_status
    t.move(tid, new_pos, new_status)
    if new_status != 'null':
        t.status(tid, new_status)


#NOTE: for sync cf
#http://blog.deeje.tv/musings/2009/06/notes-on-writing-a-history-driven-client-server-synchronization-engine.html


@get('/sync/tasks')
def get_tasks_to_sync():
    """The server renders a json of tasks he has to give
    ie: {'status': [{'id': 0, ...},] }
    """
    return t.get_unsynced()


@get('/sync/tasks/<guid>')
def get_task_from_guid(guid):
    """API to get one task's datas"""
    return t.get_from_guid(guid)


@get('/sync/faketasks')
def get_faketasks_to_sync():
    return {"b675228bf0aceac1fc64efe0d7bb207f": "2012-08-21 10:36:48"}


@get('/sync/to_sync')
def show_to_sync():
    aaa.require(role='edit', fail_redirect='/login')
    return {'local': t.sync_tasks()[0], 'remote': t.sync_tasks()[1]}
    


@get('/sync/conflicts')
def sync_conflicts():
    """The client presents a page to handle tasks conflicts
    after comparing results from http://remote/sync/tasks and
    http://localhost/sync/tasks"""
    pass


@post('/sync/tasks/<guid>')
def post_tasks_to_sync(guid):
    """The client forces the server to get new list of tasks
    ie: {'status': [{'id': 0, ...},] }
    """
    #datas = request.post.data
    #print datas
    print dir(request.json.keys())
    aaa.require(role='edit', fail_redirect='/login')
    t.save_from_json(request.json)

def is_loggued():
    try:
        u = aaa.current_user
        return True
    except:
        return False

if __name__ == '__main__':
    SimpleTemplate.defaults["is_loggued"] = is_loggued
    session_opts = {
            'session.type': 'file',
            'session.cookie_expires': 300,
            'session.data_dir': '/tmp/beaker-session',
            'session.auto': True,
            #'session.type': 'cookie',
            'session.validate_key': True
    }
    webapp = SessionMiddleware(app(), session_opts)

    # Start the Bottle webapp
    run(app=webapp, host='0.0.0.0', port=8080, debug=False, reloader=True)
