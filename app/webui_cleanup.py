#!/usr/bin/env python
import sys
import os
sys.path.extend(['lib'])
import bottle
from orgapp_globals import *
from beaker.middleware import SessionMiddleware
#from mercurial.hgweb import hgweb
from bottle import SimpleTemplate


# Use users.json and roles.json in the local example_conf directory
#subproject = hgweb('/tmp/trucmuche')
#mount('/hg/', subproject)

import bottle_werkzeug
bottle.install(bottle_werkzeug.Plugin(evalex=True))

@post('/login')
def login():
    username = request.POST.get('user', '')
    password = request.POST.get('password', '')
    _redirect = request.POST.get('redirect', '/')
    print _redirect
    auth.login(
            username,
            password,
            success_redirect=_redirect,
            fail_redirect='/truc')


@get('/login', name='login')
def login_get():
    _redirect = request.GET.get('redirect', '/')
    return template('login',
            title='Login',
            _redirect=_redirect)


@get('/logout', name='logout')
def logout():
        auth.logout(success_redirect='/login')


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




def make_wiki_menu(project, pagename=None):
    """gets a list a menus for the wiki pages"""
    menu = []
    if pagename:
        if is_logged():
            menu.append(
                {'url': url("edit_wiki_page", path=pagename, project=project),
                'title': "Edit " + pagename})
        menu.append(
            {'url': url("show_wiki_page", path=pagename, project=project),
             'title': pagename})
    menu.append(
        {'url': url("list_wiki_pages", project=project),
          'title': "List wiki pages"})
    if is_logged():
        menu.append(
            {'url': url('new_wiki_page', project=project),
              'title': "Create a new page"})
    return(menu)


@get('/<project>/doc', name="doc_index")
def doc_index(project):
    if os.path.exists(p[project].cache_path + "/Index.md"):
        return(show_wiki_page('Index.md', project))
    else:
        return(list_wiki_pages(project))


@get('/<project>/doc/List', name="list_wiki_pages")
@view('wiki/list_wiki_pages')
def list_wiki_pages(project):
    pages_list = p[project].doc.list_pages(project)
    pages_dict = [
        {'url': url("show_wiki_page", project=project, path=x),
          'title':x} for x in pages_list]
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
    _redirect = '/' + project + '/doc/' + path + '/edit',
    auth.require(
        role='edit',
        fail_redirect='/login?redirect=' + _redirect[0])
    pagename = '/' + project + '/doc/' + path
    menu = make_wiki_menu(project, path)
    content = p[project].doc.render("{0}.md".format(path), project)
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
    _redirect='/' + project + '/doc/new',
    auth.require(
        role='edit',
        fail_redirect='/login?redirect=' + _redirect[0])
    menu = make_wiki_menu(project)
    return(
        dict(
            project=project,
            title="New wiki page",
            leftmenu=menu))


@post('/<project>/doc/new')
def save_new_wiki_page(project):
    auth.require(role='edit', fail_redirect='/login')
    content = request.forms.content
    pagename = request.forms.pagename
    p[project].doc.save("{0}.md".format(pagename), content, project)
    p[project].doc.commit("{0}.md".format(pagename), project)
    p[project].doc.cache("{0}.md".format(pagename), project)
    pagename = '/' + project + '/doc/' + pagename
    redirect(pagename + "/edit")


@post('/<project>/doc/<path>/edit')
@view('wiki/edit_wiki_page')
def save_wiki_page(project, path):
    _redirect='/' + project + '/doc/' + path + '/edit',
    auth.require(
        role='edit',
        fail_redirect='/login?redirect=' + _redirect[0])
    menu = make_wiki_menu(project, path)
    content = request.forms.content
    p[project].doc.save("{0}.md".format(path), content, project)
    p[project].doc.commit("{0}.md".format(path), project)
    p[project].doc.cache("{0}.md".format(path), project)
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
    if os.path.exists('{0}/{1}'.format(p[project].doc.root_path, path)):
        return(static_file(path, root=p[project].doc.root_path))
    #else this is a rendered document
    else:
        with open(p[project].doc.cache_path + '/' + path) as _f:
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
    return dict(title='Projects list', listing=p.projects_list)


def is_logged():
    try:
        auth.current_user
        return True
    except:
        return False
import tasksui_cleanup
import codeui_cleanup

if __name__ == '__main__':
    SimpleTemplate.defaults["is_logged"] = is_logged
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
    run(app=webapp, host='0.0.0.0', port=8080, debug=True, reloader=True)
