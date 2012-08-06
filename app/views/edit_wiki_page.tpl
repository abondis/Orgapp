%def rightblock():
<form action='{{pagename}}/edit' method='post'>
  <textarea cols='80' rows='40' name='content'>{{content}}</textarea>
  <input type="submit" value="Submit" />
</form>
%end
%rebase wiki_base leftmenu=leftmenu, rightblock=rightblock, title=title
