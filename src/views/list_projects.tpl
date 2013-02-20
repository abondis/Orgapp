%from bottle import url
%def rightblock():
  <div class="span3 offset3 projects">
    <ul class="nav nav-tabs nav-stacked">
      %def walk_list_of_list(_list):
        %for l in _list:
          %if type(l) == type([]):
            <ul>
            %walk_list_of_list(l)
            </ul>
          %else:
          <li>
            <a href="{{url('doc_index', project=l)}}">{{l}}</a>
          </li>
          %end
        %end
      %end
      %walk_list_of_list(listing)
    </ul>
  </div>
%end
%rebase columns leftmenu=[], rightblock=rightblock, title=title, project=None
