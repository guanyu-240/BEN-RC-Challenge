import ConfigParser
from data import EventData
from datetime import datetime

def convert_date_str(s):
  return datetime.strptime(s, '%Y-%m-%d').date()

class EventConfig:
  def __init__(self, cfg_file):
    self.cfg = ConfigParser.RawConfigParser()
    self.cfg.read(cfg_file)

  def get_events(self):
    return self.cfg.sections() 

  def get_event_data(self, event_name):
    start_date = convert_date_str(self.cfg.get(event_name, 'start_date'))
    end_date = convert_date_str(self.cfg.get(event_name, 'end_date'))
    data_file = self.cfg.get(event_name, 'data_file')
    return EventData(data_file, start_date, end_date)
  
