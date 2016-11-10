#!/usr/bin/python

import json
from date import datetime
from strava import convert_datestr

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
  def __init__(file_name, start_date, end_date)
    fr = open(file_name)
    self.__data = json.loads(fr.read())
    fr.close()
    self.__startDate = start_date
    self.__endDate = end_date

  def add_athlete(first_name, last_name, athlete_id):
    """
    Add an athlete
    """
    entry = {'first_name': first_name,
             'last_name': last_name,
             'activities': [None for i in range(1+self.__endDate-self.__startDate)]}
    self.__data[athlete_id] = entry
    
  def add_activity(strava_activity):
    """
    Add an activity
    """
    activity_id = strava_activity['id']
    athlete_id = strava_activity['athlete']['id']
    gender = strava_activity['athlete']['sex']
    distance = strava_activity['distance']
    avg_pace = strava_activity['average_pace']
    activity_date = convert_datestr(strava_activity['start_date']).date
    if activity_date > self.__endDate or activity_date < self.__startDate:
      return False
    if (gender == "M" and avg_pace > 11.0) or \
      (gender == "F" and avg_pace > 12.0) or \
      distance < 3.0:
      return False
    athlete = self.__data.get('athlete_id')
    if athlete is None: return False
    activities = athlete['activities']
    if activities[activity_date-self._startDate] is None:
      activities[activity_date-self._startDate] = {activity_id: distance}
    else: activities[activity_date-self._startDate][activity_id] = distance
    return True
