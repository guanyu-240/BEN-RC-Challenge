#!/usr/bin/python

import os
from json import JSONEncoder,JSONDecoder
from datetime import datetime,date
from stravalib.strava import convert_datestr

"""
Event data json format:
{
strava_id:
  {
  first_name: string
  last_name: string
  activities: 
    [{<strava_activity_id, int>:milage}]
  }
}
"""
class EventData:
  def __init__(self, file_name, start_date, end_date):
    self.__dataFile = file_name
    if os.path.isfile(file_name):
      fr = open(file_name)
      json_str = fr.read()
      if json_str is None or json_str == "":
        self.__data = {}
      else: self.__data = JSONDecoder().decode(json_str)
      fr.close()
    else:
      self.__data = {}
    self.__startDate = start_date
    self.__endDate = end_date

  def add_athlete(self, first_name, last_name, athlete_id):
    """
    Add an athlete
    """
    if str(athlete_id) in self.__data: return
    entry = {'first_name': first_name,
             'last_name': last_name,
             'activities': [None for i in range(1+(self.__endDate-self.__startDate).days)]}
    self.__data[str(athlete_id)] = entry

  def register_athlete(self, first_name, last_name, strava_club_members):
    """
    Register an athlete to this event
    """
    for member in strava_club_members:
      if member['firstname'].lower() == first_name.lower() and \
           member['lastname'].lower() == last_name.lower():
        self.add_athlete(first_name, last_name, member['id']) 
    
  def add_activity(self, strava_activity):
    """
    Add an activity
    """
    activity_id = strava_activity['id']
    athlete_id = strava_activity['athlete']['id']
    gender = strava_activity['athlete']['sex']
    distance = strava_activity['distance']
    avg_pace = strava_activity['avg_pace']
    activity_date = convert_datestr(strava_activity['start_date']).date()
    if activity_date > self.__endDate or activity_date < self.__startDate:
      return False
    if (gender == "M" and avg_pace > 11.0) or \
      (gender == "F" and avg_pace > 12.0) or \
      distance < 3.0:
      return False
    athlete = self.__data.get(str(athlete_id))
    if athlete is None: return False
    activities = athlete['activities']
    idx = (activity_date-self.__startDate).days
    if activities[idx] is None:
      activities[idx] = {activity_id: distance}
    else: activities[idx][str(activity_id)] = distance
    return True

  def save_data(self):
    fr = open(self.__dataFile, 'w')
    fr.write(JSONEncoder().encode(self.__data))
    fr.close()
