#!/usr/bin/python

import sqlite3

conn =  sqlite3.connect('ben.db')

def execute_sql_query():
  cursor = conn.cursor()
  cursor.execute(sql)
  return cursor

def execute_sql_write(conn, sql):
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def createAthletesTable():
  sql = '''create table athletes
            (strava_id INTEGER,
             first_name TEXT,
             last_name TEXY)'''
  execute_sql_write(sql)

