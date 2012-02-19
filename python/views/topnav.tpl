<head>
			<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.17/themes/base/jquery-ui.css" type="text/css" media="all" />
			<link rel="stylesheet" href="http://static.jquery.com/ui/css/demo-docs-theme/ui.theme.css" type="text/css" media="all" />
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

</head>
<div class="row" >
  % menu=['wiki','tasks','home']
  % for m in menu:
  <div class='twocol'>
    <a href="/{{m}}">{{m}}</a> 
  </div>
  % end
</div>
