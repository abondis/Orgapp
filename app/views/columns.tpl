%rebase layout title=title
<leftblock>
  %def leftblock():
    <ul>
    %for m in leftmenu:
      <li><a href='{{m["url"]}}'>{{m['title']}}</a></li>
    %end
    </ul>
  %end
  %leftblock()
</leftblock>
<rightblock>
  %rightblock()
</rightblock>
