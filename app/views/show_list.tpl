%def rightblock():
  <ul id="listing">
  %def walk_list_of_list(_list):
    %for l in _list:
      %if type(l) == type([]):
      %  walk_list_of_list(l)
      %else:
      <li class="ui-state-default">
        %for x in str(l).split('\n'):
          {{x}}<br>
        %end
      </li>
      %end
    %end
  %end
  %walk_list_of_list(listing)
  </ul>
%end
%rebase columns leftmenu=leftmenu, rightblock=rightblock, title=title
