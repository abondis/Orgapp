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
  <ul class="nav nav-tabs nav-stacked">
      %if not current_path.endswith('/code/browse'):
      %  stripped_path = os.path.split(current_path)[0]
      <li>
        <a href='{{stripped_path}}'>
            ..
        </a>
      </li>
      %end
      %if current_branch is not None:
        %for x in listing[0]:
        <li>
          <a href='{{current_path}}/{{x}}'>
              {{x}}
          </a>
        </li>
        %end
        %for x in listing[1]:
        <li>
          <a href='{{current_path}}/{{x}}/show'>
              {{x}}
          </a>
        </li>
        %end
      %else:
        <li>
            Nothing has yet been done on this repo
        </li>
      %end
  </ul>
%end
%rebase columns leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
