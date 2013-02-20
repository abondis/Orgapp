%def rightblock():
  <form action='/tasks/add' method='POST' class="form-horizontal span9">
    <div class="well">
        <div class="control-group">
            <label for="title" class="control-label">Title</label>
            <div class="controls">
                <input name="name" type="text" placeholder="Title" id="title" class="span6"/>
            </div>
        </div>
        <div class="control-group">
            <label class="control-label" for="status">Description:</label>
            <div class="controls">
              <textarea name="description" placeholder="Description" class="span6" rows="10"></textarea>
            </div>
        </div>
        <div class="control-group">
            <label class="control-label" for="status">Status:</label>
            <div class="controls">
                <select name="status">
                  %for o in statuses:
                  <option value="{{o.name}}">{{o.name}}</option>
                  %end
                </select>
            </div>
        </div>
        <div class="control-group">
            <label class="control-label" for="project">Project:</label>
            <div class="controls">
                <select name="project">
                  %for p in projects:
                  <option value="{{p.name}}">{{p.name}}</option>
                  %end
                </select>
            </div>
        </div>
        <div class="control-group">
            <div class="controls">
                <input value="Create" type="submit" class="btn btn-primary" />
            </div>
        </div>
  </form>
%end
%rebase tasks/tasks leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
