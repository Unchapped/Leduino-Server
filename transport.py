#!/usr/bin/python3
import paho.mqtt.client

#MQTT Topics associated with each node
#leduino/ID/power //set 1 or 0 for off/on
#leduino/ID/channel/INDEX //Instantly set a Channel value 0-255


#TODO: Change float to (ms, uint32 (little endian))
#leduino/ID/queue //enqueue a keyframe (human readable) Expects "[delay(float)]:channel 0 [int], channel 1 [int], ..."

#TODO:
#leduino/ID/binqueue //enqueue a sparce keyframe Expects "[delay(ms, uint32 (little endian))]:[chid(char)val(char)][chid(char)val(char)]..."

binqueue_fmt = '<Lcc'

#publishes:
#leduino/ID/status //refresh at 2 hz, 0-255 uint8[16] array
#leduino/ID/announce //online/LWT messages. either "up" or "down"




class LeduinoClient(paho.mqtt.client.Client):

	# The callback for when the client receives a CONNACK response from the server.
	#def _on_connect(client, userdata, flags, rc):
	#	print("Connected with result code "+str(rc))
	#	# Subscribing in on_connect() means that if we lose the connection and
	#	# reconnect then subscriptions will be renewed.

	# The callback for when a PUBLISH message is received from the server.
	#def _on_message(client, userdata, msg):
	#	print(msg.topic+" "+str(msg.payload))

	def connect(self):
		super().connect(self.host, self.port, 60)

	def __init__(self, host, port):
		super().__init__()
		self.host = host
		self.port = port

	def send_keyframe(self, keyframe):
		#break down keyframe into node_UD:(chan, val), (chan, val), (chan, val) structure

		#for node:
		#	buf = struct.pack('<L', keyframe.delay)
		#	offset = len(buf)
		#	for channel in node.values:
		#		struct.pack_into(buf, '<cc', offset, channel.id, channel.value)
		#		offset = offset + 2
		#	self.publish('/leduino/' + node.id +'/binqueue', buf)



if __name__ == "__main__":
	client1 = LeduinoClient('localhost', 1883)
	client1.connect()
	#client1.subscribe("leduino/#")

	#client2 = LeduinoClient('localhost', 1883)
	#client2.connect()
	
	while True:
		try: 
			#client2.publish("leduino/dbg", "hello2")
			#client2.loop()
			client1.publish("leduino/dbg", "hello1")
			client1.loop()
		except KeyboardInterrupt:
			break
	client1.disconnect()
	#client2.disconnect()