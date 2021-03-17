import configparser
from data import EventData
from datetime import datetime

def convert_date_str(s):
  return datetime.strptime(s, '%Y-%m-%d').date()

class EventConfig:
  def __init__(self, cfg_file):
    self.__cfgFile = cfg_file
    self.__cfg = configparser.RawConfigParser()
    self.__cfg.read(cfg_file)
    self.events = {}
    self.__load_events()

  def __load_events(self):
    """
    Load events from the config file
    """
    event_ids = self.__cfg.sections()
    for e_id in event_ids:
      self.__addToMap(e_id)

  def __addToMap(self, e_id):
     event_type = None if not self.__cfg.has_option(e_id, 'event_type') \
                  else self.__cfg.getint(e_id, 'event_type')
     if self.__cfg.has_option(e_id, 'event_title') and \
        self.__cfg.has_option(e_id, 'start_date') and \
        self.__cfg.has_option(e_id, 'end_date') and \
        self.__cfg.has_option(e_id, 'data_file'):
        self.events[e_id] = { \
            'title': self.__cfg.get(e_id, 'event_title'),
            'start_date': convert_date_str(self.__cfg.get(e_id, 'start_date')),
            'end_date': convert_date_str(self.__cfg.get(e_id, 'end_date')),
            'event_type': event_type,
            'data_file': self.__cfg.get(e_id, 'data_file'),
            'data': None}

  def load_event_data(self, e_id):
    """
    Load event data instance into the memory,
    If the instance is already loaded, just return it,
    otherwise load it from JSON data file
    """
    ret = None
    if e_id not in self.events: return ret
    ret = self.events[e_id].get('data')
    if ret is None:
      ret = EventData(self.events[e_id]['data_file'],
                      self.events[e_id]['start_date'],
                      self.events[e_id]['end_date'],
                      self.events[e_id]['event_type'])
      self.events[e_id]['data'] = ret
    return ret

  def add_event(self, event_id, event_title, start_date, end_date):
    """
    Add an event
    """
    if event_id is None or \
       event_title is None or \
       start_date is None or \
       end_date is None: return False
    self.__cfg.add_section(event_id)
    self.__cfg.set(event_id, 'event_title', event_title)
    self.__cfg.set(event_id, 'start_date', start_date)
    self.__cfg.set(event_id, 'end_date', end_date)
    self.__cfg.set(event_id, 'data_file', event_id+'.json')
    self.__addToMap(event_id)

  def save_cfg(self):
    self.__cfg.write(cfg_file)
