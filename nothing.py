from flask import render_template, Blueprint

nothing = Blueprint('nothing', __name__)

@nothing.route('/pateint_video')
def pateint_video():
    return render_template('index1.html')  # HTML with video view

def register_socketio_events(socketio):
    @socketio.on('video_frame')
    def handle_video_frame(data):
        # Forward to all viewers (doctor/family)
        from flask_socketio import emit
        emit('broadcast_frame', data, broadcast=True)
