#!/usr/bin/python
from flask import Flask, request, render_template
from stravalib.strava import Strava
from event import get_event_data 

app = Flask(__name__)

data = get_event_data('event.cfg', 'running_streak_1')
strava_obj = Strava('d575147b36c3611231ca55f807307f16d06c8eef')

@app.route("/event_register")
def event_register():
  return render_template('event_registration.html')

@app.route("/event_stats", methods=['GET','POST'])
def event_stats():
  week_idx = data.get_current_week_idx('US/Eastern')
  if request.method == 'POST':
    week_idx = int(request.form.get('week_idx'))
  weekly_data = data.get_weekly_data(week_idx)
  return render_template('event_stats.html', weekly_data=weekly_data)

if __name__ == "__main__":
  app.run()
