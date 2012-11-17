Model
-----
- Tasks:
    - title
    - md5
    - creation date
    - last modification
    - project
    - status
    - position
- Projects:
    - id
    - name
- Statuses:
    - id
    - name

Objects
-------
- Tasklist(Project='*'):
    - Model.Tasks.filter_by(Project)
        .order_by(Model.Tasks.position)
        .group_by(Model.Statuses)
- Project:
    - Tasklist
    - Repo(config.path, config.type)
    - Documents(Repo, Type)
- Documents:
    - path
    - render
    - cache
    - create/modify
- Repo:
    - Type
    - Path
    - commit
- Orgapp:
    - Tasklist('*')
    - Projects([config.projects])
