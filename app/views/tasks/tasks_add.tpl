%def rightblock():
  <form action='/tasks/add' method='POST' class="form-horizontal">
    <div class="well">
        <div class="control-group">
            <label class="control-label" for='name'>Name:</label>
            <div class="controls">
                <input name='name' type='text'/>
            </div>
        </div>

        <div class="control-group">
            <label class="control-label" for='status'>Status:</label>
            <div class="controls">
                <select name='status'>
                  %for o in statuses:
                  <option value="{{o.name}}">{{o.name}}</option>
                  %end    
                </select>
            </div>
        </div>
    </div>
    <input value='Create' type='submit' class="btn" />
  </form>
%end
%rebase tasks/tasks leftmenu=leftmenu, rightblock=rightblock, title=title
