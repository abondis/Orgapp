
%def leftblock():
  <ul>
    <li>Wiki menu entry</li>
    <li>Wiki menu entry2</li>
    <li>Wiki menu entry3</li>
  </ul>
%end
%def rightblock():
<form action='{{pagename}}/edit' method='post'>
  <textarea cols='80' rows='40' name='content'>
{{content}}
  </textarea>
  <input type="submit" value="Submit" />
</form>
%end
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
