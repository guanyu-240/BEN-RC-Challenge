#!/usr/bin/python
import sys
from flask import Flask, render_template
from flask import request, redirect, url_for, session
from stravalib.strava import Strava, process_activity
from event import EventConfig 
from admin import AdminDB
import ConfigParser
from datetime import datetime
from pytz import timezone
from bcrypt import gensalt

app = Flask(__name__)
app.secret_key = gensalt(20)
event_data_map = {}

# load website info
cfg = ConfigParser.RawConfigParser()
cfg.read('website.cfg')
access_token = cfg.get('website', 'strava_access_token')
club_id = cfg.getint('website', 'club_id')
onload_event = cfg.get('website', 'onload_event')

# load events info
event_cfg = EventConfig('event.cfg')
events = event_cfg.events
event_cfg.load_event_data(onload_event)
strava_obj = Strava(access_token)

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
  if last_updated_time and (now - last_updated_time).seconds < 60: return
  activities = strava_obj.getClubActivitiesCurWeek(club_id, time_zone='US/Eastern')
  for a in activities:
    try:
      a = process_activity(a)
      data.add_activity(a)
    except:
      print "Error in update:", sys.exc_info()[0]
      continue
  data.update_weekly_scores(data.get_current_week_idx(time_zone='US/Eastern'))
  data.save_data()
  last_updated_time = now

def get_post_val(default_val, key):
  """
  Get the value with the given key in a 'POST' request
  """
  val = request.form.get(key)
  if val is None: return default_val
  return val
  
def get_events_list():
  """
  Return the list of events
  """
  today = datetime.now(timezone('US/Eastern')).date()
  ret_data=[]
  for e_id, e_info in events.iteritems():
    state = 'active' if today >= e_info['start_date'] else 'disabled'
    ret_data.append((e_id, e_info['title'], e_info['start_date'], e_info['end_date'], state))
  ret_data = sorted(ret_data, key=lambda x: x[2])
  return ret_data

"""
App routes
"""
# handle the requests for static files, including css or images
@app.route('/static/<path:path>')
def static(path):
    return send_from_directory('static', path)


# home page
@app.route("/events_home", methods=["GET"])
def events_home():
  ret_data = get_events_list()
  return render_template('events_home.html', events=ret_data)


# event register
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


# event statistics
@app.route("/event_stats", methods=['GET','POST'])
def event_stats():
  event_id = get_post_val(onload_event, 'event_id')
  event = events.get(event_id)
  if event is None: return "Event not found!"
  data = event_cfg.load_event_data(event_id)
  if data is None: return 'Event data not available'
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


# homepage of admin portal
@app.route("/events_admin", methods=['GET', 'POST'])
def events_admin():
  username = session.get('username')
  admin_name = session.get('admin_name')
  if not (username and admin_name):
    return redirect(url_for('admin_login'))
  if request.method == 'GET':
    ret_data = get_events_list()
    return render_template('events_admin.html', events=ret_data)
  else:
    event_id = get_post_val(None, 'event_id')
    if not event_id: return "Event not found!"
    data = event_cfg.load_event_data(event_id)
    if not data: return "Event data unavailable!"
    session['event_id'] = event_id
    for x in data.pending_activities:
      print x
    return render_template('events_admin.html', 
                               event_id=event_id,
                               pending_activities=data.pending_activities)


# pending activity approval/reject actions
@app.route("/activity_approval", methods=['POST'])
def activity_approval():
  username = session.get('username')
  admin_name = session.get('admin_name')
  if not (username and admin_name):
    return redirect(url_for('admin_login'))
  event_id = session.get('event_id')
  if not event_id: return "Event not found!"
  data = event_cfg.load_event_data(event_id)
  if not data: return "Event data unavailable!"
  activity_id = get_post_val(None, 'activity_id')
  approve = get_post_val(None, 'approve')
  if approve == 'yes':
    data.approve_pending_activity(activity_id)
    data.save_data()
  else: data.reject_pending_activity(activity_id)
  return render_template('events_admin.html', 
                             event_id=event_id,
                             pending_activities=data.pending_activities)


# admin login page/login actions
@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
  session.clear()
  if request.method == 'POST':
    username = get_post_val(None, 'username')
    password = get_post_val(None, 'password')
    admin = admin_db.login_auth(username, password)
    if not admin:
      ret_msg = "Admin does not exist, or wrong password. Try again!"
      return render_template('admin_login.html', ret_msg=ret_msg)
    session['username'] = username
    session['admin_name'] = admin['first_name'] + ' ' + admin['last_name']
    return redirect(url_for('events_admin'))
  else:
    return render_template('admin_login.html')




if __name__ == "__main__":
  app.run()
