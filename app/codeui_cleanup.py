#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['lib'])
from bottle import request
from bottle import view, url
from bottle import get
from cleanup import Tasks
from cork import Cork
import mercurial.commands as hg
from mercurial import ui, localrepo
from dulwich import repo
from doc import Doc


t = Tasks()
d = Doc()
d.cache_all()
hgui = ui.ui()
auth = Cork('config')


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
            content = d.r[project].get_object(path_sha[0])
            content = content.as_raw_string().split('\n')
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
        hg.locate(hgui, d.r[project], branch=s['branch'])
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
        l = hg.locate(hgui, d.r[project], branch=s['branch'])
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
