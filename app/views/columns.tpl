%rebase layout title=title
<leftblock>
  %def leftblock():
    <ul class="nav nav-pills">
    %for m in leftmenu:
      <li><a class="" href='{{m["url"]}}'>{{m['title']}}</a></li>
    %end
    </ul>
  %end
  %leftblock()
</leftblock>
<rightblock>
  %rightblock()
</rightblock>
