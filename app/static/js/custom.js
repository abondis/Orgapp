$(function() {
    $( ".tasks" ).sortable({
      connectWith: ".connectedSortable",
      stop: function(event, ui) {
        var tid = ui.item.attr('id');
        var new_pos = ui.item.index();
        var new_status = ui.item.parent().parent().attr('id');
        if(old_pos == new_pos) {
          new_pos = null;
        }
        if(old_status == new_status) {
          new_status = null;
        }
        var url = '/tasks/'+tid+'/update?new_pos='+new_pos+'&new_status='+new_status;
        $.ajax(url);
      },
      start: function(event, ui) {
        old_pos = ui.item.index();
        old_status = ui.item.parent().parent().attr('id');
      }
    }).disableSelection();
  });
