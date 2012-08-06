%def rightblock():
  %for p in pages_list:
    <a href="{{p['url']}}">{{p['title']}}</a>
  %end
%end
%rebase wiki_base leftmenu=leftmenu, rightblock=rightblock, title=title
