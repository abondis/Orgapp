%from bottle import url
%responsive = url('static', path='scss/responsive.css')
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="{{responsive}}"/>
    <title>{{title or 'No Title'}}</title>
  </head>
  <body>
    %include
  </body>
</html>
