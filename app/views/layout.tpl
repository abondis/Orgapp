%from bottle import url
%responsive = url('static', path='scss/responsive.css')
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="{{responsive}}"/>
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
