%from bottle import url
%def rightblock():
  <ul id="listing">
  %def walk_list_of_list(_list):
    %for l in _list:
      %if type(l) == type([]):
      <ul>
      %  walk_list_of_list(l)
      </ul>
      %else:
      <li class="ui-state-default">
      <a href="{{url('doc_index', project=l)}}">{{l}}</a>
      </li>
      %end
    %end
  %end
  %walk_list_of_list(listing)
  </ul>
%end
%rebase columns leftmenu=[], rightblock=rightblock, title=title, project=None
