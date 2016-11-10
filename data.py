#!/usr/bin/python

import json

"""
Event data json format:
{
strava_id:
  {
  first_name: string
  last_name: string
  activities: 
    [{strava_activity_id:milage}]
  }
}
"""
def load_data(file_name):
  fr = open(file_name)
  ret = json.loads(fr.read())
  fr.close()
  return ret

def add_activity(data, strava_activity):
  activity_id = strava_activity['id']
  athlete_id = strava_activity['athlete']['id']
  gender = strava_activity['athlete']['sex']
  distance = strava_activity['distance']
  avg_pace = strava_activity['average_pace']
  if (gender == "M" and avg_pace > 11.0) or \
     (gender == "F" and avg_pace > 12.0) or \
     distance < 3.0:
    return
  
