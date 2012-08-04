%def leftblock():
  <ul>
    <li>Wiki menu entry</li>
    <li>Wiki menu entry2</li>
    <li>Wiki menu entry3</li>
  </ul>
%end
%def rightblock():
{{!content}}
%end
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
