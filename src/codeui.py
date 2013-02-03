#!/usr/bin/env python
#-=- encoding: utf-8 -=-
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

from bottle import request
from bottle import view, url
from bottle import get
from orgapp import o
from ui_common import auth


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
    branch = s['branch']
    s['branch'], l = o[project].r.list_commits(branch)
    branches = o[project].r.get_branches()
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
    branch = s['branch']
    print 'branch = ' + branch
    s['branch'], content = o[project].r.get_content(path, branch)
    branches = o[project].r.get_branches()
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
    branch = request.query.branch or s.get('branch', None)
    branches = o[project].r.get_branches()
    s['branch'], hierarchy = o[project].r.get_tree(branch, path)
    menu = make_code_menu(project, path)
    return(
        dict(
            current_path=current_path,
            listing=hierarchy,
            leftmenu=menu,
            branches=branches,
            project=project,
            current_branch=s['branch'],
            title="Show tree"))
