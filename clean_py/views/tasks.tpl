<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.17/jquery-ui.min.js" type="text/javascript"></script>
<script src="http://jquery-ui.googlecode.com/svn/tags/latest/external/jquery.bgiframe-2.1.2.js" type="text/javascript"></script>
<script src="http://jquery-ui.googlecode.com/svn/tags/latest/ui/minified/i18n/jquery-ui-i18n.min.js" type="text/javascript"></script>
<style>
	#sortable { list-style-type: none; margin: 0; padding: 0; width: 60%; }
	#sortable li { margin: 0 3px 3px 3px; padding: 0.4em; padding-left: 1.5em; font-size: 1.4em; height: 18px; }
	#sortable li span { position: absolute; margin-left: -1.3em; }
</style>
<script>
	$(function() {
		$( "#sortable" ).sortable();
		$( "#sortable" ).disableSelection();
	});
</script>

%def leftblock():
<div class='threecol'>
  Left Block Menu ...
</div>
%end
%def rightblock():

<div class='sixcol'>
  <ul id="sortable">
  %i = 0
  %for t in tasks:
  <li class="ui-state-default"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>
    {{t}}
    <form method='POST' action='/tasks/done'>
      <button type='submit' name='pos' value='{{i}}'>Done</button>
    </form>
  </li>
    %i = i +1
  %end
  </ul>
  <form method="POST" action="/tasks/add">
    <input name="title"     type="text" />
    <input type="submit" />
  </form>
</div>
%end

%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
