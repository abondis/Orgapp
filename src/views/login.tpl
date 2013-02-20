<div class="row-fluid">
    <div class="well span4 offset4">
        <h1>Please login to continue</h1>
        <form action="/login?redirect={{_redirect}}" method="POST" class="form-horizontal">
            <div class="control-group">
              <label for="user" class="control-label">Username</label>
              <div class="controls">
                <input type="text" name="user" id="user"/>
              </div>
            </div>
            <div class="control-group">
              <label for='password' class="control-label">Password</label>
              <div class="controls">
                <input type="password" name="password" id="password"/>
              </div>
            </div>
            <div class="control-group">
              <div class="controls">
                <input name='redirect' value='{{_redirect}}' style='display: none;'/>
                <input type="submit" value="Submit" class="btn btn-primary">
              </div>
            </div>
        </form>
    </div>
</div>
%rebase layout title=title, project=''
