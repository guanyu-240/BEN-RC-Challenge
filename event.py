import ConfigParser
from data import EventData
from datetime import datetime

def convert_date_str(s):
  return datetime.strptime(s, '%Y-%m-%d').date()

class Event:
  def __init__(self, cfg_file, event_name):
    cfg = ConfigParser.RawConfigParser()
    cfg.read(cfg_file)
    start_date = convert_date_str(cfg.get(event_name, 'start_date'))
    end_date = convert_date_str(cfg.get(event_name, 'end_date'))
    data_file = cfg.get(event_name, 'data_file')
    self.data = EventData(data_file, start_date, end_date)
    
  
