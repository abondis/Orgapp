%def rightblock():
  %for s in tasks_list.keys():
  <tasklist id={{s}}>
    <h1>{{s}}</h1>
    <ul class="connectedSortable tasks ui-sortable well">
      %for t in tasks_list[s]:
      <li id={{t.id}} class="ui-state-default well" data-position="{{t.position}}" data-status="{{t.status_id}}">
        <button class="button btn-mini"><span class="icon icon-tasks"></span></button>
        <span class="name">{{t.name}}</span>
        <span class="position">{{t.position}}</span>
        <div class="btn-group">
            <a href="#" class="btn btn-mini"><span class="icon icon-pencil">&nbsp;</span></a>
            <a href="#" class="btn btn-mini"><span class="icon icon-trash">&nbsp;</span></a>
        </div>
      </li>
      %end
    </ul>
  </tasklist>
  %end
%end
%rebase tasks/tasks leftmenu=leftmenu, rightblock=rightblock, title=title
