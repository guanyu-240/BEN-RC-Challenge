#!/usr/bin/python
import sys
from flask import Flask, render_template
from flask import request, redirect, url_for, session
from stravalib.strava import Strava, process_activity
from stravalib.strava_oauth2 import StravaAuth
from event import EventConfig 
from admin import AdminDB
import configparser
from datetime import datetime
from pytz import timezone
from bcrypt import gensalt

app = Flask(__name__)
app.secret_key = gensalt(20)
event_data_map = {}

# load website info
cfg = configparser.RawConfigParser()
cfg.read('website.cfg')
refresh_token = cfg.get('website', 'strava_refresh_token')
club_id = cfg.getint('website', 'club_id')
event_id = cfg.get('website', 'onload_event')
auth = StravaAuth("auth.cfg")
strava_obj = Strava()

# load events info
event_cfg = EventConfig('event.cfg')
events = event_cfg.events
event_cfg.load_event_data(event_id)

# load admin info
admin_db = AdminDB('admins.cfg')

last_updated_time = None 


def update_data(data):
  """
  Query data from Strava server and make updates.
  Restricted by the limit of Strava server,
  the website can only make at most 600 requests every 15 minutes
  Here just set the updating frequency to be 1 min.
  If there are 3 data instances, if instance-1 update at '2016-11-20 0:00',
  any other instance can not make query/updates before '2016-11-20 0:01'
  """
  global last_updated_time
  now = datetime.now()
  if last_updated_time and (now - last_updated_time).seconds < 60:
    return
  data.update_activities(strava_obj, auth, 'US/Eastern')
  data.update_weekly_scores(data.get_current_week_idx(time_zone='US/Eastern'))
  data.save_data()
  last_updated_time = now

def get_post_val(default_val, key):
  """
  Get the value with the given key in a 'POST' request
  """
  val = request.form.get(key)
  if val is None:
    return default_val
  return val
  
def get_events_list():
  """
  Return the list of events
  """
  today = datetime.now(timezone('US/Eastern')).date()
  ret_data=[]
  for e_id, e_info in events.items():
    state = 'active' if today >= e_info['start_date'] else 'disabled'
    ret_data.append((e_id, e_info['title'], e_info['start_date'], e_info['end_date'], state))
  ret_data = sorted(ret_data, key=lambda x: x[2])
  return ret_data

"""
App routes
"""

# home page
@app.route("/events_home", methods=["GET"])
def events_home():
  ret_data = get_events_list()
  return render_template('events_home.html', events=ret_data)

# Authorize
@app.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    event = events.get(event_id)
    if event is None:
      return "Event not found!"
    data = event_cfg.load_event_data(event_id)
    if data is None:
      return 'Event data not available'
    event_title = event['title']
    return render_template('register.html', event_title=event_title)
  else:
    return redirect(auth.auth_url())

# Token exchange
@app.route("/token_exchange", methods=["GET"])
def token_exchange():
  code = request.args.get('code')
  scope = request.args.get('scope')
  if not code or not scope: # Access denied
    return "Access denied!"
  else:
    auth_res = auth.token_exchange(code)
    if 'athlete' not in auth_res:
      return auth_res
    event = events.get(event_id)
    if event is None:
      return "Event not found!"
    data = event_cfg.load_event_data(event_id)
    if data:
      ret = data.register_athlete(auth_res)
      data.save_data()
    return render_template("event_registration.html")
    

# event statistics
@app.route("/event_stats", methods=['GET','POST'])
def event_stats():
  event = events.get(event_id)
  if event is None:
    return "Event not found!"
  data = event_cfg.load_event_data(event_id)
  if data is None:
    return 'Event data not available'

  event_title = event['title']
  week_idx = data.get_current_week_idx('US/Eastern')
  week_idx = int(get_post_val(week_idx, 'week_idx'))

  update_data(data)
  last_week_idx = data.numWeeks-1
  week_idx = min(max(week_idx, 0), last_week_idx)
  weekly_data = data.get_weekly_data(week_idx)
  return render_template('event_stats.html', \
                             event_id=event_id, \
                             event_title=event_title, \
                             week_str=weekly_data[0], \
                             weekly_data=weekly_data[1], \
                             week_idx=week_idx, \
                             last_week_idx=last_week_idx)


if __name__ == "__main__":
  app.run()
