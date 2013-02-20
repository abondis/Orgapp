%def rightblock():
<form action='/{{project}}/doc/new' method='post' class="well horizontal-form span4">
  <h1>Create a wiki page</h1>
  <input type='text' name='pagename' placeholder="Page name..." class="span12"/><br />
  <textarea name='content' class="span12" rows="10"></textarea><br />
  <input type="submit" value="Create" class="btn btn-primary"/>
</form>
%end
%rebase wiki/wiki_base project=project, leftmenu=leftmenu, rightblock=rightblock, title=title
