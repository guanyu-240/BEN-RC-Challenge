#!/usr/bin/python
from flask import Flask, request, render_template
from stravalib.strava import Strava, process_activity
from event import get_event_data 
from multiprocessing import Process
import ConfigParser
import time

app = Flask(__name__)

data = get_event_data('event.cfg', 'running_streak_1')
cfg = ConfigParser.RawConfigParser()
cfg.read('website.cfg')
access_token = cfg.get('website', 'strava_access_token')
club_id = cfg.getint('website', 'club_id')
strava_obj = Strava(access_token)

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

def update_data():
  activities = strava_obj.getClubActivitiesCurWeek(club_id, time_zone='US/Eastern')
  for a in activities:
    a = process_activity(a)
    data.add_activity(a)
  data.update_weekly_scores(data.get_current_week_idx())
  data.save_data()

def update_data_process():
  while True:
    update_data()
    print "Updated"
    time.sleep(500)

p = Process(target=update_data_process)
p.start()
p.join()


if __name__ == "__main__":
  app.run()
