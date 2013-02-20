%from bottle import url
%bootstrap = url('static', path='bootstrap/docs/assets/css/bootstrap.css')

%bs_jquery      = url('static', path='bootstrap/docs/assets/js/jquery.js')
%bs_transition  = url('static', path='bootstrap/docs/assets/js/bootstrap-transition.js')
%bs_alert       = url('static', path='bootstrap/docs/assets/js/bootstrap-alert.js')
%bs_modal       = url('static', path='bootstrap/docs/assets/js/bootstrap-modal.js')
%bs_dropdown    = url('static', path='bootstrap/docs/assets/js/bootstrap-dropdown.js')
%bs_scrollspy   = url('static', path='bootstrap/docs/assets/js/bootstrap-scrollspy.js')
%bs_tab         = url('static', path='bootstrap/docs/assets/js/bootstrap-tab.js')
%bs_tooltip     = url('static', path='bootstrap/docs/assets/js/bootstrap-tooltip.js')
%bs_popover     = url('static', path='bootstrap/docs/assets/js/bootstrap-popover.js')
%bs_button      = url('static', path='bootstrap/docs/assets/js/bootstrap-button.js')
%bs_collapse    = url('static', path='bootstrap/docs/assets/js/bootstrap-collapse.js')
%bs_carousel    = url('static', path='bootstrap/docs/assets/js/bootstrap-carousel.js')
%bs_typeahead   = url('static', path='bootstrap/docs/assets/js/bootstrap-typeahead.js')
%jq_ui          = url('static', path='js/jquery-ui-1.9.2.custom.min.js')
%jq_ui_touch    = url('static', path='js/jquery.ui.touch-punch.min.js')
%custom_js      = url('static', path='js/custom.js')
%tasks_js       = url('static', path='js/tasks.js')
%jq_theme       = url('static', path='jquery.ui.theme.css')
%style          = url('static', path='stylesheets/screen.css')
%style_ie       = url('static', path='stylesheets/ie.css')
%style_print    = url('static', path='stylesheets/print.css')
%assets         = url('static', path='bootstrap/docs/assets/')

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href='http://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'>
    <link href="{{bootstrap}}" rel="stylesheet">
    <link href="{{assets}}css/bootstrap-responsive.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{{jq_theme}}"/>
    <link media="screen, projection" rel="stylesheet" type="text/css" href="{{style}}" />
    <link media="print" rel="stylesheet" type="text/css" href="{{style_print}}" />
    <!--[if IE]>
        <link href="{{style_ie}}" media="screen, projection" rel="stylesheet" type="text/css" />
    <![endif]-->


    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="{{assets}}ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="{{assets}}ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="{{assets}}ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="{{assets}}ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="{{assets}}ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body
  % if is_logged():
      class="logged-in"
  % end
  >

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">{{project if project else 'orgapp'}}</a>
          <div class="nav-collapse">
              <ul class="nav">
                %if 'project' in locals() and project:
                  <li>
                  <a href="{{url('doc_index', project=project)}}">Doc/Wiki</a>
                  </li>
                  <li><a href="{{url('show_tree', project=project)}}">Code</a></li>
                %else:
                  <li>
                  <a href="{{url('projects_list')}}">List projects</a>
                  </li>
                %end
                <li>
                  <a href="{{url('tasks')}}">Task</a>
                </li>
                <li>
                %if is_logged():
                  <a href="{{url('logout')}}">Logout</a>
                %else:
                  <a href="{{url('login')}}">Login</a>
                %end
                </li>
              </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container-fluid">
        %include
    </div> <!-- /container -->

    <script src="{{bs_jquery}}"></script>     
    <script src="{{bs_transition }}"></script>
    <script src="{{bs_alert}}"></script> 
    <script src="{{bs_modal}}"></script>      
    <script src="{{bs_dropdown}}"></script>   
    <script src="{{bs_scrollspy}}"></script>  
    <script src="{{bs_tab}}"></script>        
    <script src="{{bs_tooltip}}"></script>    
    <script src="{{bs_popover}}"></script>    
    <script src="{{bs_button}}"></script>     
    <script src="{{bs_collapse}}"></script>   
    <script src="{{bs_carousel}}"></script>   
    <script src="{{bs_typeahead}}"></script>  
    <script src="{{jq_ui}}"></script>
    <script src="{{jq_ui_touch}}"></script>
    <script src="{{custom_js}}"></script>
    <script src="{{tasks_js}}"></script>
  </body>
</html>
