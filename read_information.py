import os, sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from configparser import ConfigParser


file_read = ConfigParser()
file_read.read(r"secret_information.ini")

URL_IU_ALL_GR = file_read.get("IUBIP", "URL_IU_ALL_GR")
URL_IU_GR = file_read.get("IUBIP", "URL_IU_GR")
TOKEN = file_read.get("BOT", "TOKEN")