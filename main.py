import eventlet
eventlet.monkey_patch()

from __init__ import create_app, socketio
from database import db
from nothing import register_socketio_events 

app = create_app()

with app.app_context():
    db.create_all()

register_socketio_events(socketio)  

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
