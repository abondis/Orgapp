#!/usr/bin/env python
import sqlite3
import macaron
import inspect

class Tasks(macaron.Model): pass

class Positions(macaron.Model): pass

class Orgapp(object):
  def __init__(self):
    macaron.macaronage("tasks.db")


  def prompt(self):
    """ Simple prompt box """
    while True:
      try:
        command = raw_input('enter something:\n')
      except:
        break
      #parse command
      cls = command.split(' ')
      if len(cls):
        _command_name = cls[0]
        if hasattr(self, _command_name):
          _command_obj = getattr(self, _command_name)
          _args = len(inspect.getargspec(_command_obj).args)
          print('args len: {0}'.format(_args))
          if _args > 1:
            #call command
            _command_obj(*cls[1:])
          else:
            _command_obj()

  def ls(self):
    print [(x.id, x.name, x.position) for x in Tasks.all().order_by('position')]

  def add(self,name, dest):
    # create the Task
    _task = Tasks.create(name = name)
    _task.position = dest
    macaron.bake()
    # give it a Position

  def rm(self, source):
    pass
  def move(self, source, dest):
    # TODO:
    # a1 b2 c3 d4 e5
    # a1  2 c3 d4 b5 e6 <== (move b 4)
    # a1 c2 d3 b4 e5 <==  between source and dest: position -1
    macaron.execute('UPDATE tasks SET position = position + 1 WHERE id != {0} AND position >= {1}'.format(source, dest))
    macaron.execute('UPDATE tasks SET position = {1} WHERE id = {0}'.format(source, dest))
    macaron.bake()



if __name__=='__main__': 
  #create table tasks( id INTEGER PRIMARY KEY, name text, context text);
  #create table positions( id INTEGER PRIMARY KEY, taskid NUMERIC, position NUMERIC, foreign key(taskid) references tasks(id));
  t = Orgapp()
  t.prompt()
