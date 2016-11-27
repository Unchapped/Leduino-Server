
from peewee import *
import os

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

__all__ = [] #TODO: make this right!


class Channel(Model):
	name = CharField() #human-readable Channel name
	node = CharField() #MQTT Node ID, 4 bit Hex
	channel = IntegerField()
	color = CharField(default = 'w') #should be 'r','g','b' or default to 'w'.
	class Meta:
		database = _db #can this be double inherited?
		primary_key = CompositeKey('name', 'color')
	def __repr__(self):
		return self.name + ':' + self.node + '/' + str(self.channel)

class ColorChannel(_BaseModel):
	#TODO: add a constructor that overrides/creates "anonymous" internal channels
	name = CharField(unique=True, index=True) #human-readable Channel name
	#r = ForeignKeyField(Channel, to_field='name', null = False, related_name='parent')
	#g = ForeignKeyField(Channel, to_field='name', null = False, related_name='parent')
	#b = ForeignKeyField(Channel, to_field='name', null = False, related_name='parent')
	#def __repr__(self):
	#	return self.name + '(RGB Color): (' + self.r.node + '/' + str(self.r.channel) + "," + self.g.node + '/' + str(self.g.channel) + "," + self.b.node + '/' + str(self.b.channel) + ')'


#TODO: we need to manually create an additional foreign key for rgb channels on the db to add r, g and b objects to a Colorchannel
#db.create_foreign_key(User, User.favorite_post)

class Keyframe(_BaseModel):
	delay = TimeField()

class KeyValue(_BaseModel):
	channel = ForeignKeyField(Channel, to_field='name', null = False, related_name='keyvals')
	value = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
	keyframe = ForeignKeyField(Keyframe, null = False, related_name='values')

class ColorKeyValue(_BaseModel):
	channel = ForeignKeyField(ColorChannel, to_field='name', null = False, related_name='keyvals')
	r = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
	g = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
	b = IntegerField() #0 to 255 TODO: should this be float 0 -> 1?
	keyframe = ForeignKeyField(Keyframe, null = False, related_name='rgb_values')



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
	_db.create_tables([Channel, ColorChannel, Keyframe, KeyValue, ColorKeyValue], safe=True)

if __name__ == "__main__":
	import os
	#execute unit tests...
	os.remove('test.db') # don't use _db_name in case we're in some weird off-nominal case and using the main db
	create()
	test_c = Channel.create(name='test_c', node='0000', channel=3)
	test_r = Channel.create(name='test', node='0000', channel=1, color='r')
	test_g = Channel.create(name='test', node='0000', channel=0, color='g')
	test_b = Channel.create(name='test', node='0000', channel=2, color='b')
	test_rgb = ColorChannel.create(name='test')
	for c in Channel:
		print(c)
	#for r in RGBChannel:
	#	print(r)
	close()