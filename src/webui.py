#!/usr/bin/env python
#
#This file is part of Orgapp.
#
#Orgapp is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Orgapp is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Orgapp.  If not, see <http://www.gnu.org/licenses/>.

import os
import bottle
from orgapp import o
from ui_common import auth
from bottle import run, static_file, request
from bottle import view, redirect, template, url
from bottle import post, get
from bottle import app
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
    print(_redirect)
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
    if os.path.exists(o[project].cache_path + "/Index.md"):
        return(show_wiki_page('Index.md', project))
    else:
        return(list_wiki_pages(project))


@get('/<project>/doc/List', name="list_wiki_pages")
@view('wiki/list_wiki_pages')
def list_wiki_pages(project):
    pages_list = o[project].doc_files.cache_list()
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
    # get raw content
    # FIXME: how to not force .md?
    # find a way to identify rendered cache and map it to their original
    # - cache only render-able content
    # - put render somewhere different
    # - keep the extension for cached file
    # - use db :(
    content = o[project].doc_files.get_doc(path + '.md', False)
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
    _redirect = '/' + project + '/doc/new',
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
    o[project].create_doc(pagename, content, 'md')
    pagename = '/' + project + '/doc/' + pagename
    redirect(pagename + "/edit")


@post('/<project>/doc/<path>/edit')
@view('wiki/edit_wiki_page')
def save_wiki_page(project, path):
    _redirect = '/' + project + '/doc/' + path + '/edit',
    auth.require(
        role='edit',
        fail_redirect='/login?redirect=' + _redirect[0])
    menu = make_wiki_menu(project, path)
    content = request.forms.content
    o[project].create_doc(path, content, 'md')
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
    # ie: they both have an extension
    if o[project].doc_files.is_static(path):
        return(static_file(path, root=o[project].doc_files.root_path))
    #else this is a rendered document
    # .md -> no ext
    else:
        content = o[project].doc_files.get_doc(path)
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
    return dict(title='Projects list', listing=o.projects.keys())


def is_logged():
    try:
        auth.current_user
        return True
    except:
        return False

# import routes for tasks and codes
import tasksui
import codeui

if __name__ == '__main__':
    SimpleTemplate.defaults["is_logged"] = is_logged
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 30000,
        'session.data_dir': '/tmp/beaker-session',
        'session.auto': True,
        #'session.type': 'cookie',
        'session.validate_key': True
    }
    webapp = SessionMiddleware(app(), session_opts)

    # Start the Bottle webapp
    run(app=webapp, host='0.0.0.0', port=8080, debug=True, reloader=True)
