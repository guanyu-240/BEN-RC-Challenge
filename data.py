#!/usr/bin/python

from __future__ import print_function
import os, sys
from decimal import Decimal
from json import JSONEncoder, JSONDecoder
import json
from datetime import datetime, date, timedelta
import calendar, time
from stravalib.strava import Strava, process_activity, convert_datestr
from stravalib.strava_oauth2 import StravaAuth
from pytz import timezone

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

TYPE_MILEAGE = 1
TYPE_STREAK = 2

TEAMS = "teams"
ATHLETES = "athletes"


class EventData:
    def __init__(self, file_name, start_date, end_date, event_type):
        self.__dataFile = file_name
        if os.path.isfile(file_name):
            fr = open(file_name)
            json_str = fr.read()
            if json_str is None or json_str == "":
                self.__data = {TEAMS: {}, ATHLETES: {}}
            else:
                self.__data = JSONDecoder().decode(json_str)
            fr.close()
        else:
            self.__data = {TEAMS: {}, ATHLETES: {}}
        self.__startDate = start_date
        self.__endDate = end_date
        self.__type = TYPE_MILEAGE if not event_type else event_type
        self.numDays = 1 + (self.__endDate - self.__startDate).days
        self.numWeeks = int(self.numDays / 7)

    def register_athlete(self, auth_res):
        """
        Add an athlete
        """
        athlete = auth_res["athlete"]
        if str(athlete["id"]) in self.__data:
            self.__data[ATHLETES][str(athlete["id"])]["access_token"] = auth_res["access_token"]
            self.__data[ATHLETES][str(athlete["id"])]["refresh_token"] = auth_res["refresh_token"]
            self.__data[ATHLETES][str(athlete["id"])]["token_expires_at"] = auth_res["expires_at"]
        else:
            entry = {
                "first_name": athlete["firstname"],
                "last_name": athlete["lastname"],
                "gender": athlete["sex"],
                "access_token": auth_res["access_token"],
                "refresh_token": auth_res["refresh_token"],
                "token_expires_at": auth_res["expires_at"],
                "activities": [None for i in range(self.numDays)],
                "weekly_scores": [0 for i in range(self.numWeeks)],
                "total_mileage": 0,
                "avg_pace": -1,
            }
            self.__data[ATHLETES][str(athlete["id"])] = entry
        self.save_data()

    def get_teams(self):
        return self.__data[TEAMS]

    def register_or_join_team(self, athlete_id, team_id, team_name):
        """
        Add team
        """
        if team_name:
            # register a new team
            team_id = team_name.lower().replace(" ", "_")
            if team_id in self.__data[TEAMS]:
                return None
            self.__data[TEAMS][team_id] = team_name

        self.__data[ATHLETES][str(athlete_id)]["team_id"] = team_id
        self.save_data()
        return team_id

    def get_current_week_idx(self, time_zone="UTC"):
        today = datetime.now(timezone(time_zone)).date()
        ret = int((today - self.__startDate).days / 7)
        return min(max(ret, 0), self.numWeeks)

    def update_weekly_streak_scores(self, week_idx):
        """
        Calculate weekly running streak score for all athletes
        """
        if week_idx >= self.numWeeks:
            return
        for k, v in self.__data[ATHLETES].items():
            activities = v["activities"]
            base_score = 0
            penalty = 0
            drought = 0
            for i in range(7):
                if activities[week_idx * 7 + i] is None:
                    drought += 1
                else:
                    base_score += 1
                    if drought > 0:
                        penalty += drought - 1
                    drought = 0
            if drought > 0:
                penalty += drought - 1
            score = min(max(base_score - penalty, 0), 6)
            v["weekly_scores"][week_idx] = score

    def update_weekly_mileages(self, week_idx):
        """
        Calculate weekly mileages for all athletes
        """
        if week_idx >= self.numWeeks:
            return
        for k, v in self.__data[ATHLETES].items():
            activities = v["activities"]
            mileages = 0.0
            for i in range(7):
                if activities[week_idx * 7 + i] is not None:
                    for a_id, m in activities[week_idx * 7 + i].items():
                        mileages += float(m[0])
            v["weekly_scores"][week_idx] = round(mileages, 2)

    def update_total_mileage(self):
        for k, v in self.__data[ATHLETES].items():
            activities = v["activities"]
            mileage = 0.0
            total_time = 0.0
            for i in range(len(activities)):
                if activities[i] is not None:
                    for a_id, m in activities[i].items():
                        try:
                            mileage += float(m[0])
                            total_time += float(m[1])
                        except:
                            print(
                                v["first_name"] + " " + v["last_name"], file=sys.stderr
                            )
            v["total_mileage"] = round(mileage, 1)
            avg_pace = 0 if mileage == 0 else total_time / (60 * mileage)
            pace_min = int(avg_pace)
            pace_sec = int(60 * (avg_pace - pace_min))
            v["avg_pace"] = "{:d}:{:02d}".format(pace_min, pace_sec)

    def update_weekly_scores(self, week_idx):
        if self.__type == TYPE_MILEAGE:
            self.update_weekly_mileages(week_idx)
        elif self.__type == TYPE_STREAK:
            self.update_weekly_streak_scores(week_idx)

    def get_weekly_data(self, week_idx):
        """
        Get the data of the given week index
        Including the distances on all 7 days and adjusted scores
        for all the participants
        """
        ret = []
        if week_idx >= self.numWeeks or week_idx < 0:
            return ["Week:", []]
        week_start = self.__startDate + timedelta(week_idx * 7)
        week_end = week_start + timedelta(6)
        week_str = (
            "Week: {0.month}/{0.day}/{0.year} - {1.month}/{1.day}/{1.year}".format(
                week_start, week_end
            )
        )
        for k, v in self.__data[ATHLETES].items():
            workouts = v["activities"][7 * week_idx : 7 * week_idx + 7]
            workouts_stats = []
            for x in workouts:
                if x:
                    distance = 0.0
                    for i, m in x.items():
                        try:
                            distance += m[0]
                        except:
                            print(
                                v["first_name"] + " " + v["last_name"], file=sys.stderr
                            )
                    workouts_stats.append("{0:.1f}".format(distance))
                else:
                    workouts_stats.append("")
            total_score = sum(Decimal(i) for i in v["weekly_scores"])
            if self.__type == TYPE_MILEAGE:
                total_score = round(total_score, 2)
            entry = {
                "name": v["first_name"] + " " + v["last_name"],
                "workouts": workouts_stats,
                "score": v["weekly_scores"][week_idx],
                "total_score": total_score,
                "total_mileage": v.get("total_mileage", 0),
                "avg_pace": v.get("avg_pace", -1),
            }
            ret.append(entry)
        return [week_str, ret]
    
    def get_teams_data(self):
        teams_mileage = {}
        for k,v in self.__data[ATHLETES].items():
            if "team_id" in v:
                team_id = v["team_id"]
                athlete_name = f"{v['first_name']} {v['last_name']}"
                if team_id not in teams_mileage:
                    teams_mileage[team_id] = [v["total_mileage"], [athlete_name]]
                else:
                    teams_mileage[team_id][0] += v["total_mileage"]
                    teams_mileage[team_id][1].append(athlete_name)
        res = []
        for k,v in teams_mileage.items():
            res.append((k, self.__data[TEAMS][k], v[0], v[1], v[0]/len(v[1])))
        res = sorted(res, key=lambda x: x[4], reverse=True)
        return res

    def update_activities(self, strava_obj, auth, time_zone):
        """
        Update athlete activities
        """
        for athlete_id, athlete_stats in self.__data[ATHLETES].items():
            current_time = int(time.time())
            expires_at = int(athlete_stats["token_expires_at"])
            if expires_at - current_time <= 3600:
                auth_res = auth.refresh_token(athlete_stats["refresh_token"])
                if "access_token" in auth_res:
                    athlete_stats["access_token"] = auth_res["access_token"]
                    athlete_stats["token_expires_at"] = auth_res["expires_at"]
                else:
                    err_msg = "Authentication on Athlete %s %s failed %s" % (
                        athlete_stats["first_name"],
                        athlete_stats["last_name"],
                        str(activities),
                    )
                    print(err_msg, file=sys.stderr)
                    continue
            activities = strava_obj.listAthleteActivities(
                athlete_stats["access_token"],
                current_time,
                current_time - 864000,
                None,
                200,
            )
            if not isinstance(activities, list):
                err_msg = "Authentication on Athlete %s %s failed %s" % (
                    athlete_stats["first_name"],
                    athlete_stats["last_name"],
                    str(activities),
                )
                print(err_msg, file=sys.stderr)
                continue
            for activity in activities:
                if "run" not in activity["type"].lower():
                    continue
                activity = process_activity(activity)
                self.add_activity(athlete_stats, activity, time_zone)

    def add_activity(self, athlete_stats, strava_activity, time_zone):
        """
        Add an activity
        An activity is considered invalid if
        Pace > 11 min/mile for a male athlete
        Pace > 12 min/mile for a female athlete
        If the activity is manual, add it to the pending queue
        """
        if strava_activity["manual"]:
            err_msg = "Activity %s by %s %s is not qualified" % (
                strava_activity["id"],
                athlete_stats["first_name"],
                athlete_stats["last_name"],
            )
            print(err_msg, file=sys.stderr)
            print(json.dumps(strava_activity), file=sys.stderr)
            return False
        activity_id = strava_activity["id"]
        gender = athlete_stats["gender"]
        distance = strava_activity["distance"]
        moving_time = strava_activity["moving_time"]
        avg_pace = strava_activity["avg_pace"]
        activity_date = convert_datestr(strava_activity["start_date"], time_zone).date()
        if activity_date > self.__endDate or activity_date < self.__startDate:
            return False
        if (
            (gender == "M" and avg_pace > 11.0)
            or (gender == "F" and avg_pace > 12.0)
            or distance < 3.0
        ):
            return False
        activities = athlete_stats["activities"]
        idx = (activity_date - self.__startDate).days
        """
    if activities[idx] and str(activity_id) in activities[idx]:
      return False
    """
        if activities[idx] is None:
            activities[idx] = {str(activity_id): [distance, moving_time]}
        else:
            activities[idx][str(activity_id)] = [distance, moving_time]
        return True

    def save_data(self):
        """
        Save the data to the file
        """
        fr = open(self.__dataFile, "w")
        fr.write(JSONEncoder().encode(self.__data))
        fr.close()
