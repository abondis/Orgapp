#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import macaron
import inspect
import sys
import os
sys.path.extend(['../lib'])
#from config_parser import orgappConfigParser
from config_parser import configure
from md5 import md5
from datetime import datetime


class SetGuid(macaron.AtCreate):
    def set(self, obj, value):
        return md5(str(datetime.now())).hexdigest()

class Status(macaron.Model):
    pass


class Tasks(macaron.Model):
    status = macaron.ManyToOne(Status)
    guid = SetGuid()
    last_modified = macaron.TimestampAtSave()


@configure
class Orgapp(object):
    def __init__(self):
        if not os.path.exists(self.path):
            import setup_db
            setup_db.init_db(self.path)
        macaron.macaronage(self.path)

    def prompt(self):
        """                                                  'Simple prompt box """
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
                if _args > 1:
                    #call command
                    _command_obj(*cls[1:])
                else:
                    print(_command_obj())

    def ls(self):
        #print(Tasks.all().count())
        tasks_list = {}
        #get statuses
        for s in Status.all():
            tasks_list[s.name] = Tasks.select("status_id=?",
                                              [s.id]).order_by('position')
            #render dict of lists
            # 'status': ['task1', 'task2']
        return(tasks_list)

    def add(self, name, dest=None, status='new'):
        if not dest:
            dest = Tasks.all()
            #print dest
            if dest:
                dest = dest.count()
            else:
                dest = 0
        status_id = Status.get('name=?', [status]).id
        Tasks.create(name=name, position=dest, status_id=status_id)
        # create the Task
        #self.move(_task.id, dest)
        macaron.bake()
        # give it a Position

    def rm(self, source):
        # FIXME: removes everything
        Tasks.get(source).delete()
        macaron.bake()

    def status(self, sourceid, status):
        _source = Tasks.get(sourceid)
        _source.status_id = Status.get('name=?', [status]).id
        _source.save()

    def move(self, sourceid, destid, status):
        # TODO: clean
        src_pos = Tasks.get(sourceid).position
        status_id = Status.get('name=?', [status]).id
        if int(destid) == 0:
            dst_pos = 0
            macaron.execute("""
                            UPDATE tasks
                            SET position = position + 1
                            WHERE id != {0}
                            AND position >= {1}
                            AND status_id = {2}""".format(
                                sourceid,
                                dst_pos,
                                status_id))
            macaron.execute("""
                            UPDATE tasks
                            SET position = {1}
                            WHERE id = {0}""".format(
                                sourceid,
                                dst_pos))
        else:
            dst_pos = Tasks.get(destid).position
            if src_pos < dst_pos:
                macaron.execute("""
                                UPDATE tasks
                                SET position = position - 1
                                WHERE id != {0}
                                AND position > {1}
                                AND position <= {2}
                                AND status_id = {3}""".format(
                                    sourceid,
                                    src_pos,
                                    dst_pos,
                                    status_id))
                macaron.execute("""
                                UPDATE tasks
                                SET position = {1}
                                WHERE id = {0}""".format(
                                    sourceid,
                                    dst_pos))
            else:
                macaron.execute("""
                                UPDATE tasks
                                SET position = position + 1
                                WHERE id != {0}
                                AND position > {2}
                                AND position < {1}
                                AND status_id = {3}""".format(
                                    sourceid,
                                    src_pos,
                                    dst_pos,
                                    status_id))
                macaron.execute("""
                                UPDATE tasks
                                SET position = {1}
                                WHERE id = {0}""".format(
                                    sourceid,
                                    dst_pos + 1))
                macaron.bake()

    def position(self, sourceid):
        return Tasks.get(sourceid).position

    def get_statuses(self):
        return Status.all()

    """Sync:
    1- add guid to task when created
    2- get all guid on client with mtime since last sync
    3- get all guid on server with mtime since last sync
    4- keep 2 dict, to_send, to_receive
    5- call server/update with to_send
    6- call localhost/update with to_receive
    """

    def add_to_history(self):
        """add any db action to the history"""
        pass

    def get_last_synced(self):
        """gets datetime of last sync"""
        pass

    def get_unsynced(self):
        """Gets unsynced entries
        brute force: get all"""
        # get entries where history.date > get_last_synced
        return Tasks.all()

    def save_unsynced(self):
        """Saves unsynced data
        brute force: take everything replace everything"""
        pass

if __name__ == '__main__':
    t = Orgapp()
    t.prompt()
