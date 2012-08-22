%def rightblock():
  <form>
    <select onchange="document.location.href = document.URL.split('?')[0] + '?branch=' + this.value ">
    %for o in branches:
      %if o == current_branch:
        <option selected="selected" value='{{o}}'>{{o}}</option>
      %else:
        <option value='{{o}}'>{{o}}</option>
      %end
    %end
    </select>
  </form>
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
%rebase columns leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
