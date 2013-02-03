%def rightblock():
<ol class='code'>
  %idx = 1
  %for l in content:
  <li><code class='codeline-{{idx%2}}'>{{l}}</code></li>
  %idx += 1
  %end
</ol>
%end
%rebase columns leftmenu=leftmenu, rightblock=rightblock, title=title, project=project
