block
%def leftblock():
leftblock content
<div style='width: 200px; float: left'>
  %for p in files:
     <a href={{page}}/../{{p}}>{{p}}</a><br/>
  %end
</div>
-----
<br/>
%end
%rebase columns title=page, leftblock=leftblock, content=content
