import os
import re

class taskList(object):
  def __init__(self, filename):
    self.filename = filename
    self.doneFile = "%s.done" % filename
    self.tasks = []
    self.contexts = set()
    self.projects = set()
    # dictionnaire clef -> regex
    self.setParser()
    self.populateTasks(filename)
  
  def populateTasks(self, filename):
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
    for l in self.tasks:
      if l.endswith('\n'): end = ''
      else: end = '\n'
      f.write(l+end)
    f.close() 

  def moveTask(self, source, destination):
    """ moves a task number `source` before task number `destination`
    """
    self.tasks.insert(destination-1, self.tasks.pop(source-1))
    self.updateTaskList()

  def addTask(self, taskString, destination=None):
    """ adds a task to our tasklist, default to the end of the list
    """
    if not destination:
      self.tasks.append(taskString)
    else:
      self.tasks.insert(destination-1, taskString)
    self.updateTaskList()
  
  def setParser(self):
    self.reContext = re.compile('@\w+')
    self.reProject = re.compile('\+\w+')
    #self.taskname = re.compile('((?![+@]\w+))?[ \n]\w+')
    self.taskname = re.compile("(^|[+@]\w+\s?)(.*)(\s?[+@]\w+|$)")

  def parseTaskList(self):
    for x in self.tasks:
      self.context.add(self.reContext(x))
      self.project.add(self.reProject(x))   

  def __repr__(self):
    return("\n".join(self.tasks))

  def listTasks(self):
    cpt = 1
    for l in self.tasks:
      print("%d: %s" % (cpt, l)) 
      cpt += 1
  
  def searchBy(fn):
    """ Decorator for other search functions
        takes:
        - self
        - the tag prefix tagMark (ie: '+')
        - the tag's name tagName (ie: 'aproject')
    """
    def _inner(*args, **kwargs):
      self, tagMark, tagName = fn(*args, **kwargs)
      searchResults = []
      for element in self.tasks:
        if tagMark + tagName in element:
          searchResults.append(element)
      return searchResults
    return _inner

  @searchBy
  def searchByProject(self, project):
     projectTagMark = '+'
     return self, projectTagMark, project

  @searchBy
  def searchByContext(self, context):
     contextTagMark = '@'
     return self, contextTagMark, context

  @searchBy
  def searchByTask(self, task):
     taskTagMark = ''
     return self, taskTagMark, task

  def ponderate(self):
    """ shows the tasks in order of preference, ie:
    - priority, createdate"""
    pass
  
  def documentTask(self, taskName):
    """ creates a file/folder for each task
    """
    pass

  def markAsDone(self, task):
    """ mark a task as done
    """
    doneTask = self.tasks.pop(task)
    self.updateTaskList()
    if not os.path.exists(self.doneFile):
      f = open(self.doneFile, 'w')
      f.close()
    elif not os.path.isfile(self.doneFile):
      raise("Filename %s is not a file" % self.doneFile)
      return 1
    f = open(self.doneFile, 'a')
    f.write("%s\n" %  doneTask)
    f.close()
