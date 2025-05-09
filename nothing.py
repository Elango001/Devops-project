from flask import Blueprint, render_template
from flask_socketio import SocketIO, emit
from deepface import DeepFace
import base64
from io import BytesIO
from PIL import Image
import numpy as np

nothing = Blueprint('nothing', __name__)

@nothing.route('/pateint_video')
def pateint_video():
    return render_template('new.html')  # HTML with video view

def register_socketio_events(socketio):
    @socketio.on('video_frame')
    def handle_video_frame(data):
        try:
        # Decode the base64 image (data['frame'] contains the base64 string)
            img_data = base64.b64decode(data['frame'].split('base64,')[1])
            img = Image.open(BytesIO(img_data))  # Open image from the binary data

        # Convert image to numpy array (for DeepFace)
            img_array = np.array(img)

        # Analyze the emotion using DeepFace, with enforce_detection=False to skip face detection
            analysis = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)

        # Extract the dominant emotion from the analysis
            dominant_emotion = analysis[0]['dominant_emotion']

        # Emit the detected emotion back to the client
            emit('broadcast_frame', {'emotion': dominant_emotion}, broadcast=True)

        except Exception as e:
            print(f"Error processing frame: {e}")
            emit('broadcast_frame', {'emotion': 'error'}, broadcast=True)  # Handle errors gracefully
