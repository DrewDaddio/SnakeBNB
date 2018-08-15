import mongoengine

#this is how we'll create the connection
#this file is called from the program python file in the services folder
def global_init():
    mongoengine.register_connection(alias='core', name='snake_bnb')
