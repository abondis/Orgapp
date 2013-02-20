$(function() {
    $( "body.logged-in .tasks" ).sortable({
      connectWith: ".connectedSortable",
      distance:20,
      stop: function(event, ui) {
        var tid = ui.item.attr('id');
        var new_pos = ui.item.index();
        var new_status = ui.item.parent().parent().attr('data-status-id');

        var old_pos = ui.item.attr('data-position')
        var old_status = ui.item.attr('data-status')

        if(old_status == new_status) {
          new_status = null;
        }
        var url = '/tasks/'+tid+'/update?new_pos='+new_pos+'&new_status='+new_status;

        ui.item.attr('data-position', new_pos);
        ui.item.attr('data-status', (new_status? new_status :old_status));

        ui.item.find('.position').html(new_pos);
        $.ajax(url);
      }
    }).disableSelection();
  });
