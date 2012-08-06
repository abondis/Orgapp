%def leftblock():
  <ul>
    %for m in leftmenu:
      <li>
        <a href="{{m['url']}}">{{m['title']}}</a>
      </li>
    %end
  </ul>
%end
%rightblock
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
