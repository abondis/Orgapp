%def rightblock():
  %for s in tasks_list.keys():
  <tasklist id={{s}}>
    <h1>{{s}}</h1>
    <ul class="connectedSortable tasks ui-sortable well">
      %for t in tasks_list[s]:
      <li id={{t.id}} class="ui-state-default well" data-position="{{t.position}}" data-status="{{t.status_id}}">
        {{t.name}}
        <span class="position">{{t.position}}</span>
      </li>
      %end
    </ul>
  </tasklist>
  %end
%end
%rebase tasks leftmenu=leftmenu, rightblock=rightblock, title=title
