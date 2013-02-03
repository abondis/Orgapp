%def rightblock():
  %for p in pages_list:
    <a href="{{p['url']}}">{{p['title']}}</a>
  %end
%end
%rebase wiki/wiki_base project=project, leftmenu=leftmenu, rightblock=rightblock, title=title
