#!/usr/bin/python
from flask import Flask, request, render_template
from stravalib.strava import Strava, process_activity
from event import EventConfig 
import ConfigParser
from datetime import datetime

app = Flask(__name__)
event_data_map = {}

# load website info
cfg = ConfigParser.RawConfigParser()
cfg.read('website.cfg')
access_token = cfg.get('website', 'strava_access_token')
club_id = cfg.getint('website', 'club_id')
onload_event = cfg.get('website', 'onload_event')

# load events info
event_cfg = EventConfig('event.cfg')
events = event_cfg.get_events()
event_data_map[onload_event] = event_cfg.get_event_data(onload_event)

strava_obj = Strava(access_token)

last_updated_time = datetime.now()

def update_data(data):
  global last_updated_time
  now = datetime.now()
  if (now - last_updated_time).seconds < 100: return
  activities = strava_obj.getClubActivitiesCurWeek(club_id, time_zone='US/Eastern')
  for a in activities:
    a = process_activity(a)
    data.add_activity(a)
  data.update_weekly_scores(data.get_current_week_idx())
  data.save_data()
  last_updated_time = now

def get_post_val(default_val, key):
  val = request.form.get(key)
  if val is None: return default_val
  return val
  

@app.route("/event_register", methods=['GET', 'POST'])
def event_register():
  event_id = onload_event
  if request.method == 'POST':
    event_id = onload_event
    event_id = get_post_val(event_id, 'event_id')
    first_name = get_post_val(None, 'first_name')
    last_name = get_post_val(None, 'last_name')
    data = event_data_map.get(event_id)
    if data:
      ret = data.register_athlete(first_name, last_name, strava_obj.listClubMembers(club_id))
      data.save_data()
      if ret: ret_msg = "Athlete registered successfully!"
      else: ret_msg = "Athlete already registered or not in strava group!"
    else: ret_msg = "Can not register!"
    return render_template('event_registration.html', ret_msg=ret_msg)
  else:
    return render_template('event_registration.html')

@app.route("/event_stats", methods=['GET','POST'])
def event_stats():
  event_id = onload_event
  if request.method == 'POST':
    event_id = get_post_val(event_id, 'event_id')
  data = event_data_map.get(event_id)
  week_idx = data.get_current_week_idx('US/Eastern')
  if request.method == 'POST':
    week_idx = int(get_post_val(week_idx, 'week_idx'))
  weekly_data = ['Week:', []]
  last_week_idx = 0
  if data is not None:
    update_data(data)
    last_week_idx = data.numWeeks-1
    week_idx = min(max(week_idx, 0), data.numWeeks)
    weekly_data = data.get_weekly_data(week_idx)
  return render_template('event_stats.html', \
                             event_id=event_id, \
                             week_str=weekly_data[0], \
                             weekly_data=weekly_data[1], \
                             week_idx=week_idx, \
                             last_week_idx=last_week_idx)


if __name__ == "__main__":
  app.run()
