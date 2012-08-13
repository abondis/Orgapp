%def rightblock():
  <form action='/tasks/add' method='POST'>
    <label for='name'>Name:</label>
    <input name='name' type='text'/>
    <label for='status'>Status:</label>
    <select name='status'>
      %for o in statuses:
      <option value="{{o.name}}">{{o.name}}</option>
      %end    
    </select>
    <br />
    <input value='Create' type='submit' class="btn" />
  </form>
%end
%rebase tasks/tasks leftmenu=leftmenu, rightblock=rightblock, title=title
