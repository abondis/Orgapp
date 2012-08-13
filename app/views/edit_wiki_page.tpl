%def rightblock():
<h1>{{pagename}}</h1>
<form action='{{pagename}}/edit' method='post' class="well">
  <textarea class="input-xxlarge" name='content'>{{content}}</textarea><br />
  <input type="submit" value="Submit" class="btn btn-primary" />
</form>
%end
%rebase wiki_base leftmenu=leftmenu, rightblock=rightblock, title=title
