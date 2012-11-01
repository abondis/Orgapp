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
%jq_ui          = url('static', path='js/jquery-ui-1.8.22.custom.min.js')
%jq_ui_touch    = url('static', path='js/jquery.ui.touch-punch.min.js')
%custom_js      = url('static', path='js/custom.js')
%jq_theme       = url('static', path='jquery.ui.theme.css')
%responsive     = url('static', path='scss/responsive.css')
%assets         = url('static', path='bootstrap/docs/assets/')

%aloha_js       = url('static', path='aloha/aloha-full.min.js')
%aloha_css      = url('static', path='aloha/aloha.css')

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="{{bootstrap}}" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="{{assets}}css/bootstrap-responsive.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{{jq_theme}}"/>
    <link rel="stylesheet" type="text/css" href="{{responsive}}"/>
    <link rel="stylesheet" type="text/css" href="{{aloha_css}}"/>

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

    <div class="container">
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
    <script src="{{aloha_js}}" data-aloha-plugins="common/ui,common/format,common/highlighteditables,common/link"></script>
    <script src="{{custom_js}}"></script>
    <script type="text/javascript">
        var Aloha = window.Aloha || ( window.Aloha = {} );
            
        Aloha.settings = {
               locale: 'en',
               plugins: {
               format: {
                    config: [  'b', 'i', 'p', 'sub', 'sup', 'del', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat' ],
                    editables : {
                       '#title'    : [ ]
                   }
                },
               link: {
                   editables : {
                       '#title'    : [  ]
                    }
                },
                list: {
                    editables : {
                        '#title'    : [  ]
                    }
                },
                abbr: {
                    editables : {
                        '#title'    : [  ]
                    }
                },
                image: {
                    'fixedAspectRatio': true,
                    'maxWidth': 1024,
                    'minWidth': 10,
                    'maxHeight': 786,
                    'minHeight': 10,
                    'globalselector': '.global',
                    'ui': {
                        'oneTab': false
                    },
                    editables : {
                        '#title'    : [  ]
                    }
                }
            },
            sidebar: {
                disabled: true
            },
            contentHandler: {
                allows: {
                    elements: [
                        'a', 'abbr', 'b', 'blockquote', 'br', 'caption', 'cite', 'code', 'col',
                        'colgroup', 'dd', 'del', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                        'i', 'img', 'li', 'ol', 'p', 'pre', 'q', 'small', 'strike', 'strong',
                        'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'u',
                        'ul', 'span', 'hr', 'object', 'div'
                    ],

                    attributes: {
                        'a': ['href', 'title', 'id', 'class', 'target', 'data-gentics-aloha-repository', 'data-gentics-aloha-object-id'],
                        'div': [ 'id', 'class'],
                        'abbr': ['title'],
                        'blockquote': ['cite'],
                        'br': ['class'],
                        'col': ['span', 'width'],
                        'colgroup': ['span', 'width'],
                        'img': ['align', 'alt', 'height', 'src', 'title', 'width', 'class'],
                        'ol': ['start', 'type'],
                        'q': ['cite'],
                        'p': ['class'],
                        'table': ['summary', 'width'],
                        'td': ['abbr', 'axis', 'colspan', 'rowspan', 'width'],
                        'th': ['abbr', 'axis', 'colspan', 'rowspan', 'scope', 'width'],
                        'ul': ['type'],
                        'span': ['class','style','lang','xml:lang']
                    },

                    protocols: {
                        'a': {'href': ['ftp', 'http', 'https', 'mailto', '__relative__']},
                        'blockquote': {'cite': ['http', 'https', '__relative__']},
                        'img': {'src' : ['http', 'https', '__relative__']},
                        'q': {'cite': ['http', 'https', '__relative__']}
                    }
                }
            }
         }; 
         Aloha.ready( function() {
             Aloha.jQuery('p.aloha').aloha();
         });
     </script>
  </body>
</html>
