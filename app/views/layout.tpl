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
        <li>Doc/Wiki</li>
        <li>Tasks</li>
        <li>Code</li>
      </ul>
    </topmenu>
    %include
  </body>
</html>
