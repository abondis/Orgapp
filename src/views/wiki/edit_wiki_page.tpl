%def rightblock():
<form action='{{pagename}}/edit' method='post' class="well span6">
  <h1>Edit : {{pagename}}</h1>
  <textarea class="span12" name='content' rows="10">{{content}}</textarea><br />
  <input type="submit" value="Save" class="btn btn-primary" />
</form>
%end
%rebase wiki/wiki_base leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
