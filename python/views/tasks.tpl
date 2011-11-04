%def leftblock():
<div class='threecol'>
  Left Block Menu ...
</div>
%end
%def rightblock():
<div class='sixcol'>
  %for t in tasks:
    {{t}}
  %end
</div>
%end

%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
