import os

class taskList(object):
  def __init__(self, filename):
    self.filename = filename
    self.tasks = []
    # dictionnaire clef -> regex
    self.setParser()
    self.listTasks(filename)
  
  def listTasks(self, filename):
    if not os.path.exists(filename):
      f = open(filename, 'w')
      f.close()
    elif not os.path.isfile(filename):
      raise("Filename %s is not a file" % filename)
      return 1
    f = open(filename, 'r')
    self.tasks = [ x for x in f.xreadlines() ]
    f.close()

  def updateTaskList(self):
    f = open(self.filename, 'w')
    f.writelines(self.tasks)
    f.close() 

  def moveTask(self, source, destination):
    """ moves a task number `source` before task number `destination`
    """
    self.tasks.insert(destination, self.tasks.pop(source))
    self.updateTaskList()

  def addTask(self, taskString, destination=None):
    """ adds a task to our tasklist, default to the end of the list
    """
    if not destination:
      self.tasks.append(taskString)
    else:
      self.tasks.insert(destination, taskString)
    self.updateTaskList()
  
  def setParser(self):
    self.reContext = re.compile('@\w+')
    self.reProject = re.compile('\+\w+')
    #self.taskname = re.compile('((?![+@]\w+))?[ \n]\w+')
    self.taskname = re.compile("(^|[+@]\w+\s?)(.*)(\s?[+@]\w+|$)")

  def parseTaskList(self):
   
      
    
  
