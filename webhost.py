#!/usr/bin/python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/event_register")
def event_register():
  return render_template('event_registration.html')

@app.route("/event_stats")
def event_stats():
  return render_template('event_stats.html')

if __name__ == "__main__":
  app.run()
