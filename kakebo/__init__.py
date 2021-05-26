from flask import Flask 

app = Flask(__name__, instance_relative_config=True) # instance_relative_config: crea instancia Config
app.config.from_object('config')

from kakebo import views

