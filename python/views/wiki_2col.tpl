block
%def leftblock():
leftblock content
%if not path.endswith('/'): slash = '/'
%else: slash = ''
<div style='width: 200px; float: left'>
  %for p in files:
     <a href=/{{path}}{{slash}}{{p}}>{{p}}</a><br/>
  %end
</div>
-----
<br/>
%end
%def rightblock():
  {{!content}}
%end
%rebase 2columns title=page, leftblock=leftblock, rightblock=rightblock
