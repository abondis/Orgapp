#!/usr/bin/env python
import sqlite3
import macaron

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

db = sqlite3.connect("tasks.db")
cur = db.cursor()
res = [cur.execute(query) for query in queries]
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
macaron.bake()
