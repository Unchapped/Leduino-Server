#!/usr/bin/python3
import paho.mqtt.client as mqtt
import argparse
import struct

# Parse Arguments
def parse_tuple(string):
	return tuple(map(int, string.split(':', 2)))
parser = argparse.ArgumentParser(description='send a test keyframe packet to a leduino node.')
parser.add_argument('channels', metavar='C:V', nargs='+', help='a channel:value tuple to add to the sent keyframe packet', type=parse_tuple)
parser.add_argument('-n', '--node', help='Specify which leduino node to send the keyframe to', default='0')
parser.add_argument('-d', '--delay', type=int, help='Specifies how long of a delay (ms) to apply to the keyframe fade-in', default=1000)
parser.add_argument('-s', '--server', help='The MQTT server hostname to connect to', default='localhost')
parser.add_argument('-p', '--port', help='The MQTT server port number', type=int, default=1883)
args = parser.parse_args()


# form struct buffer
msg = struct.pack('<I', args.delay)
for chval in args.channels:
	msg += struct.pack('<BB', chval[0], chval[1])

topic = 'leduino/' + args.node + '/binqueue'
print('Sending packet:', msg, 'to', topic, 'on', args.server)

#connect and send
#TODO: add better debug handling
client = mqtt.Client()
client.connect(args.server, args.port, 60)
client.publish("leduino/" + args.node + "/binqueue", msg)
client.loop()
client.disconnect()
exit(0)