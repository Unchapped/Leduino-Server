from time import sleep
from daemonize import Daemonize

import configdb

def main():
	configdb.open()
	while True:
		sleep(5)
		print('.',end='')
	configdb.close()


pid = "/tmp/test.pid"
daemon = Daemonize(app="test_app", pid=pid, action=main)
daemon.start()