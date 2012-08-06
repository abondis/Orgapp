%def leftblock():
  <ul>
    <li>Add</li>
    <li>A task action</li>
  </ul>
%end
%def rightblock():
  %for s in tasks_list.keys():
  <div>
    <h1>{{s}}</h1>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Position</th>
      </tr>
    </thead>
    <tbody>
      %for t in tasks_list[s]:
      <tr>
        <td>{{t.id}}</td>
        <td>{{t.name}}</td>
        <td>{{t.position}}</td>
      </tr>
      %end
    </tbody>
  </table>
  </div>
  %end
%end
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
