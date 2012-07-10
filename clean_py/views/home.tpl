block
%def leftblock():
leftblock content
  leftblock
%end
%def rightblock():
rightblock content
  rightblock
%end
%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
