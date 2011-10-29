%def leftblock():
<div class='threecol'>
%if not path.endswith('/'): slash = '/'
%else: slash = ''
  %for p in files:
     <a href=/{{path}}{{slash}}{{p}}>{{p}}</a><br/>
  %end
</div>
%end
%def rightblock():
<div class='sixcol'>
  {{!content}}
</div>
%end
%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
