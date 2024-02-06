from configparser import ConfigParser


file_read = ConfigParser()
file_read.read(r"iubip_les\secret_information.ini")

URL_IU_ALL_GR = file_read.get("IUBIP", "URL_IU_ALL_GR")
URL_IU_GR = file_read.get("IUBIP", "URL_IU_GR")
TOKEN = file_read.get("BOT", "TOKEN")