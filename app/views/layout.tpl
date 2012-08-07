%from bottle import url
%responsive = url('static', path='scss/responsive.css')
%jq_theme = url('static', path='jquery.ui.theme.css')
%jq = url('static', path='js/jquery-1.7.2.min.js')
%jq_ui = url('static', path='js/jquery-ui-1.8.22.custom.min.js')
%jq_ui_touch = url('static', path='js/jquery.ui.touch-punch.min.js')
%custom_js = url('static', path='js/custom.js')
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="{{responsive}}"/>
    <link rel="stylesheet" type="text/css" href="{{jq_theme}}"/>
    <script src={{jq}}></script>
    <script src={{jq_ui}}></script>
    <script src={{jq_ui_touch}}></script>
    <script src={{custom_js}}></script>
    <title>{{title or 'No Title'}}</title>
  </head>
  <body>
    <header>
      A Header!
    </header>
    <topmenu>
      <ul>
        <li>
          <a href="{{url('doc_index')}}">Doc/Wiki</a>
        </li>
        <li>
          <a href="{{url('tasks')}}">Task</a>
        </li>
        <li><a href="#">Code</a></li>
      </ul>
    </topmenu>
    %include
  </body>
</html>
