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
from datetime import timedelta, datetime
import urllib2
import json


class SetGuid(macaron.AtCreate):
    def set(self, obj, value):
        return md5(str(datetime.now())).hexdigest()


class Status(macaron.Model):
    pass


class Sync(macaron.Model):
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
        """Simple prompt box """
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
        return Sync.get(1).last_synced

    def set_last_synced(self, days=0):
        """sets datetime of last Sync"""
        _s = Sync.get(1)
        _s.last_synced = datetime.now() - timedelta(days=days)
        _s.save()
        macaron.bake()

    def get_unsynced(self):
        """Gets unsynced entries
        brute force: get all"""
        # get entries where history.date > get_last_synced
        try:
            _last_synced = datetime.strptime(self.get_last_synced(),
                    "%Y-%m-%d %H:%M:%S.%f")
        except:
            self.set_last_synced(30)
            _last_synced = datetime.strptime(self.get_last_synced(),
                    "%Y-%m-%d %H:%M:%S.%f")
        #print("type last_synced " + str(type(_last_synced)))
        #print("last synced " + str(_last_synced))
        _t = Tasks.select('last_modified > ?', [_last_synced])
        _d = {}
        if _t.count() > 0:
            for x in _t:
                _d[x.guid] = str(x.last_modified)
        return _d

    def get_remote_tasks(self, action=None):
        """Gets the json from the remote orgapp server"""
        if not action:
            url = "http://127.0.0.1:8081/sync/tasks"
        else:
            url = "http://127.0.0.1:8081/sync/" + action
        _content = urllib2.urlopen(url).read()
        _json = json.loads(_content)
        return _json

    def get_from_guid(self, guid):
        _t = Tasks.get('guid == ?', [guid])
        return {
                'name': _t.name,
                'status_id': _t.status_id,
                'position': _t.position,
                'last_modified': str(_t.last_modified)
                }

    def save_from_json(self, content):
        """Saves a task using json content"""
        try:
            _t = Tasks.get('guid == ?', [content['guid']])
            _t.position = content['position']
            _t.last_modified = content['last_modified']
            _t.name = content['name']
            _t.status_id = content['status_id']
        except:
            _t = Tasks.create(**content)
        _t.guid = content['guid']
        _t.save()
        macaron.bake()

    def sync_tasks(self):
        """defines what is to keep from remote and local and sync"""
        _local = self.get_unsynced()
        _remote = self.get_remote_tasks()
        #print "_local " + str(_local)
        for k, v in _local.items():
            #if same md5 has same date, we don't sync
            _remote_value = _remote.get(k, None)
            if _remote_value:
                if _remote_value == v:
                    _remote.pop(k)
                    _local.pop(k)
                #else if the remote date is earlier than localhost
                #we sync from remote
                elif _remote_value > _local[k]:
                    _local.pop(k)
                else:
                    _remote.pop(k)
        #print("\n\n we will sync\n" + str(_remote))
        for k in _remote.keys():
            _update = self.get_remote_tasks("tasks/" + k)
            try:
                _t = Tasks.get('guid == ?', [k])
                _t.position = _update['position']
                _t.last_modified = _update['last_modified']
                _t.name = _update['name']
                _t.status_id = _update['status_id']
            except:
                _t = Tasks.create(guid=k, **_update)
            _t.guid = k
            _t.save()
            macaron.bake()
        # send to remote
        for k in _local.keys():
            _d = {}
            _t = Tasks.get('guid == ?', [k])
            _d['name'] = _t.name
            _d['position'] = _t.position
            _d['status_id'] = _t.status_id
            _d['last_modified'] = str(_t.last_modified)
            _d['guid'] = k
            url = "http://127.0.0.1:8081/sync/tasks/" + k
            # convert json_dict to JSON
            json_data = json.dumps(_d)
            # convert str to bytes (ensure encoding is OK)
            post_data = json_data.encode('utf-8')
            # we should also say the JSON content type header
            headers = {}
            headers['Content-Type'] = 'application/json'
            # now do the request for a url
            req = urllib2.Request(url, post_data, headers)
            # send the request
            res = urllib2.urlopen(req)
            # get task details
            #send it to the remote


        return [_local, _remote]

    def save_unsynced(self):
        """Saves unsynced data
        brute force: take everything replace everything"""
        pass

if __name__ == '__main__':
    t = Orgapp()
    t.prompt()
