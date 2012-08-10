%def rightblock():
<form action='/doc/new' method='post'>
  <input type='text' name='pagename'/><br>
  <textarea cols='60' rows='30' name='content'></textarea>
  <input type="submit" value="Submit" />
</form>
%end
%rebase wiki_base leftmenu=leftmenu, rightblock=rightblock, title=title
