%def rightblock():
  %for s in tasks_list.keys():
  <tasklist id={{s}}>
    <h1>{{s}}</h1>
    <ul class="connectedSortable tasks ui-sortable well">
      %for t in tasks_list[s]:
      <li id={{t.id}} class="ui-state-default well" data-position="{{t.position}}" data-status="{{t.status_id}}">
        <span class="name">{{t.name}}</span>
        <span class="position">{{t.position}}</span>
        <div class="btn-group pull-right">
            <a href="#view-{{t.id}}"  class="btn btn-mini" role="button" data-toggle="modal"><span class="icon icon-pencil">&nbsp;</span></a>
            <a href="#" class="btn btn-mini"><span class="icon icon-trash">&nbsp;</span></a>
        </div>
        <div id="view-{{t.id}}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="Task details" aria-hidden="true">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="myModalLabel">Task</h3>
          </div>
          <div class="modal-body">
            <div class="control-group">
                <div class="controls">
                  <input type="text" placeholder="Title" value="{{t.name}}" class="btn-block"/>
                </div>
            </div>
            <div class="control-group">
                <div class="controls">
                  <textarea class="btn-block">blou</textarea>
                </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-link" data-dismiss="modal" aria-hidden="true">Close without saving</button>
            <button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">Save</button>
          </div>
        </div>
      </li>
      %end
    </ul>
  </tasklist>
  %end
%end
%rebase tasks/tasks leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
