%def leftblock():
<div class='threecol'>
%import os
%if not path.endswith('/'): slash = '/'
%else: slash = ''
  %for p in files:
     %if os.path.isdir(path+slash+p):
       %(pname,slug) = p2t[path+slash+p]
       %pname = p
     %else:
       %(pname,slug) = p2t[path+slash+p]
     %end
     <a href='/{{slug}}'>{{pname}}</a><br/>
  %end
</div>
%end
%def rightblock():
<div class='sixcol'>
  {{!content}}
</div>
%end
%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
