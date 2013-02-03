function updateTask(taskId) {
  $.post(
      '/tasks/' + taskId + '/update/ajax',
      {
          title: $('#task-title-' + taskId).html(),
          description: $('#task-description-' + taskId).html(),
      }
  );
}

function deleteTask(taskId) {
  $.post('/tasks/' + taskId + '/delete/ajax', {tid: taskId})
  .done(function() {
    $('#view-' + taskId).remove();
    $('#' + taskId).remove();
  });
}
