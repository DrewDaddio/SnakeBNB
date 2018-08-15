import datetime
import mongoengine

#these items will be configured to work with the mongoengine libraries

class Snake:
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now) #date specific for mongoengine
    species = mongoengine.StringField(required=True)

    length = mongoengine.FloatField(required=True)
    name = mongoengine.StringField(required=True)
    is_venomous = mongoengine.BooleanField(required=True)

    #below will be used for MongoDB to query this
    meta = { #meta is the dictionary name
        'db_alias': 'core', #This will look for the core table
        'collection': 'snakes' #This is where the attributes will be located. Similar to a table
    }