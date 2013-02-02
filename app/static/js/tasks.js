function updateTask(taskId) {
    $.post({
        '/tasks/' + taskId + '/update/ajax',
        {
            title: $('task-title-' + tid).html(),
            description: $('task-description-' + tid).html(),
        }
    })
}
