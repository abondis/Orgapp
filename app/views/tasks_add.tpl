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
    <input value='Create' type='submit'/>
  </form>
%end
%rebase tasks leftmenu=leftmenu, rightblock=rightblock, title=title
