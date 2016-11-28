#!/usr/bin/python3
import os
import logging

from time import sleep

#this may be redundant, see: http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/
from daemonize import Daemonize

import configdb

#this could be easily made configurable, like in octoprint
settings_dir = os.path.expanduser("~/.leduino/")

#initialize our settings directory, if it doesn't exist
try:
	os.makedirs(settings_dir)
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise

pid = "/var/run/leduinod.pid"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(settings_dir + "leduinod.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

def main():
	configdb.open()
	while True:
		sleep(5)
		logger.debug("I'm alive!")
	configdb.close()

daemon = Daemonize(app="leduinod", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()