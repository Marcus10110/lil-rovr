from flask import Flask, jsonify, send_from_directory, Response
from camera_stream import CameraStream

app = Flask(__name__, static_folder='static')

# Serve the index.html file


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# REST API Endpoint for AJAX calls


@app.route('/api/data', methods=['GET'])
def get_data():
    # Add logic to return your data
    # Example: return a simple JSON response
    return jsonify({'key': 'value'})

# Serve static files (CSS, JS)


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)


# Route for video streaming
@app.route('/video.mjpg')
def video_feed():
    def generate():
        while True:
            frame = camera_stream.get_frame()
            yield (b'--FRAME\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n' +
                   frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=FRAME')


camera_stream = CameraStream()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
