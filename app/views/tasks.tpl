%def leftblock():
  <ul>
    <li>Add</li>
    <li>A task action</li>
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
