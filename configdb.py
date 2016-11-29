#!/usr/bin/python3
from peewee import *

#our "private" database handle
#use separate db files for tests and productions
if __name__ == "__main__":
	_db_name = 'test.db'
else:
	_db_name = __name__ + '.db'

_db = SqliteDatabase(_db_name)

class ColorAggregateField(Field):
    db_field = 'uuid'

class _BaseModel(Model): #use this to define db-wide defaults
	class Meta:
		database = _db

#__all__ = [] #TODO: make this right!


class ChannelGroup(_BaseModel):
	name = CharField(primary_key = True) #human-readable Channel name

	@staticmethod
	def CreateRGBGroup(name, node, r_ch, g_ch, b_ch, group=None): #factory method for quickly creating RGB fixtures
		#todo: make this more flexible, for now, assume all channels are colocated on node
		if group is None: #allow appending to an existing group
			group = ChannelGroup.create(name = name);
		Channel.create(name=name + '_r', node=node, channel=r_ch, color='r', group=group)
		Channel.create(name=name + '_g', node=node, channel=g_ch, color='g', group=group)
		Channel.create(name=name + '_b', node=node, channel=b_ch, color='b', group=group)
		return group

	def __repr__(self):		
		retval = self.name + '(group):\n'
		for c in self.channels:
			retval += '\t' + str(c) + '\n'
		return retval

class Channel(_BaseModel):
	name = CharField(unique=True, index=True) #human-readable Channel name
	node = CharField(max_length = 4) #MQTT Node ID, 4 bit Hex
	channel = IntegerField() #Node Channel Number
	color = CharField(default = 'w', max_length = 1) #should be 'r','g','b' or default to 'w'.
	group = ForeignKeyField(ChannelGroup, related_name='channels', null=True)
	def __repr__(self):
		return self.name + ':' + self.node + '/' + str(self.channel)
	class Meta:
		# create a unique on each node/channel pair
		indexes = (
			(('node', 'channel'), True),
		)

class Keyframe(_BaseModel):
	fade = TimeField()

#
#class KeyValue(_BaseModel):
#	channel = ForeignKeyField(Channel, to_field='name', null = False, related_name='keyvals')
#	value = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
#	keyframe = ForeignKeyField(Keyframe, null = False, related_name='values')

#class ColorKeyValue(_BaseModel):
#	channel = ForeignKeyField(ColorChannel, to_field='name', null = False, related_name='keyvals')
#	r = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
#	g = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
#	b = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
#	keyframe = ForeignKeyField(Keyframe, null = False, related_name='rgb_values')


# this is out module initialization code that opens the db
def open():
	global _db
	_db.connect()

def close():
	global _db
	_db.close()

def create():
	global _db
	open()
	_db.create_tables([Channel, ChannelGroup, Keyframe], safe=True)

if __name__ == "__main__":
	import os
	import os.path
	#execute quick n' dirty tests...
	if os.path.isfile('test.db'): 
		os.remove('test.db') # don't use _db_name in case we're in some weird off-nominal case and using the main db
	create()
	test_c = Channel.create(name='test_c', node='0000', channel=3)
	group1 = ChannelGroup.CreateRGBGroup('test_group', '0000', 1, 0, 2)
	test_c2 = Channel.create(name='test_c2', node='0000', channel=5, group=group1)

	for c in Channel:
		print(c)
	print(group1)
	close()