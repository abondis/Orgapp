%rebase layout title=page
<div style='width: 200px; float: left'>
  %for p in files:
     <a href={{page}}/../{{p}}>{{p}}</a><br/>
</div>
-----
<br/>
<div>
  {{!content}}
</div>
<br/>
