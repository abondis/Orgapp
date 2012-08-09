#!/usr/bin/env python
import sqlite3
import macaron
from config_parser import orgappConfigParser


def init_db(path=None):

    if not path:
        path = orgappConfigParser.get(
            'tasks',
            'path').encode('utf-8')

    queries = ["""
    create table tasks(
      id INTEGER PRIMARY KEY,
      name TEXT,
      position NUMERIC,
      status_id INTEGER NOT NULL);""",
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

    class Status(macaron.Model):
        pass

    class Tasks(macaron.Model):
        status = macaron.ManyToOne(Status)

    Status.create(name="new")
    Status.create(name="running")
    Status.create(name="closed")
    macaron.bake()

if __name__ == "__main__":
    init_db()
