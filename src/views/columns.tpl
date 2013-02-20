%try:
  %rebase layout title=title, project=project
%except:
  %rebase layout title=title
%end

<div class="row-fluid">
    %def leftblock():
      %if leftmenu:
        <div class="col-secondary span3">
          <div class="well" >
            <ul class="nav nav-list">
              %for m in leftmenu:
                <li><a href='{{m["url"]}}'>{{m['title']}}</a></li>
              %end
          </ul>
        </div>
      </div>
      %end
    %end
    %leftblock()
  <div class="col-primary span9">
    %rightblock()
  </rightblock>
</div>
