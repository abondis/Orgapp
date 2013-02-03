function updateTask(taskId) {
    $.post(
        '/tasks/' + taskId + '/update/ajax',
        {
            title: $('task-title-' + taskId).html(),
            description: $('task-description-' + taskId).html(),
        }
    )
}
