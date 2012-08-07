%def leftblock():
  <ul>
  %for m in leftmenu:
    <li><a href='{{m["url"]}}'>{{m['title']}}</a></li>
  %end
  </ul>
%end
%def rightblock():
  %for s in tasks_list.keys():
  <tasklist id={{s}}>
    <h1>{{s}}</h1>
    <ul class="connectedSortable tasks ui-sortable">
      %for t in tasks_list[s]:
      <li id={{t.id}} class="ui-state-default">
        {{t.name}}
        {{t.position}}
      </li>
      %end
    </ul>
  </tasklist>
  %end
%end
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
