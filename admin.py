from configparser import RawConfigParser
from bcrypt import hashpw


class AdminDB:
    def __init__(self, cfg_file):
        self.__cfgFile = cfg_file
        self.__cfg = RawConfigParser()
        self.__cfg.read(cfg_file)

    def login_auth(self, username, passwd):
        """
        Login authentication
        """
        if username and passwd and self.__cfg.has_section(username):
            pwd_hash = self.__cfg.get(username, "password_hash")
            passwd = passwd.encode("utf-8")
            if hashpw(passwd, pwd_hash) == pwd_hash:
                return {
                    "first_name": self.__cfg.get(username, "first_name"),
                    "last_name": self.__cfg.get(username, "last_name"),
                    "super": self.__cfg.getboolean(username, "super"),
                }
        return None

    def save(self):
        self.__cfg.write(self.__cfgFile)
