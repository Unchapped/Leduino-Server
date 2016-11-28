#!/usr/bin/python3
import os
import logging
import logging.handlers
import argparse
import sys
import atexit

from time import sleep

#this may be redundant, see: http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/
from daemonize import Daemonize

import configdb

#Defaults
LOG_FILENAME = "/var/log/leduinod.log"
PID_FILENAME = "/var/run/leduinod.pid"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Leduino-MQTT keyframe and scheduling service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
	LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

keep_fds = [handler.stream.fileno()]

#register a handler to make sure we close our database.
#TODO: make this work?
#atexit(configdb.close)

#here's the main 'process' execute
def main():
	configdb.open()
	while True:
		sleep(5)
		logger.info("I'm alive!")
	configdb.close()

daemon = Daemonize(app="leduinod", pid=PID_FILENAME, action=main, logger=logger, keep_fds=keep_fds)
daemon.start()