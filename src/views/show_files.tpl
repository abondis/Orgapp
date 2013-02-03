%import os.path
%def rightblock():
  <form>
    <select onchange="document.location.href = document.location.protocol + '//' + document.location.host + '/{{project}}/code/browse' + '?branch=' + this.value ">
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
      %if not current_path.endswith('/code/browse'):
      %  stripped_path = os.path.split(current_path)[0]
      <a href='{{stripped_path}}'>
      <li class="ui-state-default">
          ..
      </li>
      </a>
      %end
      %if current_branch is not None:
        %for x in listing[0]:
        <a href='{{current_path}}/{{x}}'>
        <li class="ui-state-default">
            {{x}}
        </li>
        </a>
        %end
        %for x in listing[1]:
        <a href='{{current_path}}/{{x}}/show'>
        <li class="ui-state-default">
            {{x}}
        </li>
        </a>
        %end
      %else:
        <li class="ui-state-default">
            Nothing has yet been done on this repo
        </li>
      %end
  </ul>
%end
%rebase columns leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
