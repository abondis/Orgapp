import macaron
import sqlite3
db = sqlite3.connect("tasks.db")
cur = db.cursor()
cur.execute("create table tasks( id INTEGER PRIMARY KEY, name text, position NUMERIC, status_id INTEGER NOT NULL);")
cur.execute("create table status( id INTEGER PRIMARY KEY, name text);")
#except:
  #pass # handle the error

db.commit()
cur.close()
db.close()

macaron.macaronage("tasks.db")
class Status(macaron.Model): pass
class Tasks(macaron.Model):
  status = macaron.ManyToOne(Status)

Status.create(name="new")
Status.create(name="running")
Status.create(name="closed")
# Add a task
Tasks.create(name="une tache1", position=1, status_id=1)
Tasks.create(name="une tache2", position=2, status_id=1)
Tasks.create(name="une tache3", position=3, status_id=1)
Tasks.create(name="une tache4", position=4, status_id=1)
Tasks.create(name="une tache5", position=5, status_id=1)
Tasks.create(name="une tache6", position=6, status_id=1)
Tasks.create(name="une tache7", position=7, status_id=1)
Tasks.create(name="une tache8", position=8, status_id=1)
macaron.bake()
[(x.id, x.name, x.position) for x in Tasks.all()]
[(x.id, x.name, x.position, x.status.name) for x in Tasks.all()]


# get the list of positions > 1
pos = Positions.select("position>?", [1])
# update tasks set position = position + 1 where position >1;
#pos = Positions.select("position>?", [1])
# move taskid2 after task in position 3
# get tasks after position 4 only if not taskid 2
macaron.execute('UPDATE tasks SET position = position + 1 WHERE id != 2 AND position >= 4')
macaron.execute('UPDATE tasks SET position = 4 WHERE id = 2')
[(x.taskid, x.position) for x in Positions.all().order_by('position')]
#Out[138]: [(1, 1), (3, 3), (2, 4), (4, 5), (5, 6)]

# move task 6 to position 1
macaron.execute('UPDATE positions SET position = position + 1 WHERE taskid != 5 AND position >= 1')
macaron.execute('UPDATE positions SET position = 1 WHERE taskid = 5')
[(x.taskid, x.position) for x in Positions.all().order_by('position')]
#Out[143]: [(1, 2), (3, 4), (2, 5), (4, 6), (5, 7)]


#positionsToUpdate = Positions.select('position>=? and taskid != ?', [4, 2])
#for x in positionsToUpdate:
  #x.position += 1
macaron.bake()
Positions.select('taskid=?', 2).position = 4

pos = Positions.select("position>?", [4])


# print the positions > 1
print([x.position for x in pos])
# print the tasks name with positions > 1
print([Tasks.get("id=?", [x.position]).name for x in pos])
