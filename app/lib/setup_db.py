#!/usr/bin/env python
import sqlite3
import macaron
from config_parser import orgappConfigParser
from md5 import md5
from datetime import datetime


def init_db(path=None):

    if not path:
        path = orgappConfigParser.get(
            'tasks',
            'path').encode('utf-8')

    queries = ["""
    create table tasksmodel(
      id INTEGER PRIMARY KEY,
      name TEXT,
      position NUMERIC,
      guid TEXT,
      last_modified DATE,
      status_id INTEGER NOT NULL);""",
    """
    create table sync(
      id INTEGER PRIMARY KEY,
      last_synced DATE);
    """,
    """
    create table status(
      id INTEGER PRIMARY KEY,
      name TEXT);
    """]

    db = sqlite3.connect(path)
    cur = db.cursor()
    [cur.execute(query) for query in queries]
    db.commit()
    cur.close()
    db.close()

    macaron.macaronage(path)

    class SetGuid(macaron.AtCreate):
        def set(self, obj, value):
            return md5(str(datetime.now())).hexdigest()

    class Sync(macaron.Model):
        pass

    class Status(macaron.Model):
        pass

    class Tasks(macaron.Model):
        status = macaron.ManyToOne(Status)
        guid = SetGuid()
        last_modified = macaron.TimestampAtSave()

    Status.create(name="new")
    Status.create(name="running")
    Status.create(name="closed")
    Sync.create(last_synced="None")
    macaron.bake()

if __name__ == "__main__":
    init_db()
