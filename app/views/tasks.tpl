%def leftblock():
  <ul>
    <li>Add</li>
    <li>A task action</li>
  </ul>
%end
%def rightblock():
<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Name</th>
      <th>Position</th>
      <th>status</th>
    </tr>
  </thead>
  <tbody>
  %for t in tasks:
    <tr>
      <td>{{t[0]}}</td>
      <td>{{t[1]}}</td>
      <td>{{t[2]}}</td>
      <td>{{t[3]}}</td>
    </tr>
  %end
  </tbody>
</table>
%end
%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
