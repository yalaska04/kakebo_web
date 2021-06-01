from flask import Flask 

app = Flask(__name__, instance_relative_config=True) # instance_relative_config: creates instance Config

app.config.from_object('config')

# Config object provides loading of configuration files from relative filenames. 
# Instance_relative_config=True --> makes it possible to change the loading 
#   via filenames to be relative to the instance path if wanted.
# How? Flask preloads the config from a module and then overrides the config from 
#   a file in the instance folder if it exists.

from kakebo import views # import views; it's where we keep our routes

