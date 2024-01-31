import logging
from flask import Flask, jsonify, send_from_directory, Response, request
from camera_stream import CameraStream
import hardware
import steering
app = Flask(__name__, static_folder='static')

# Disable request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Serve the index.html file


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# REST API Endpoint for AJAX calls


@app.route('/api/drive', methods=['GET'])
def get_data():
    # take two parameters from the request: direction (number, -90 to +90) and speed (number, -1 to 1)
    direction_arg = request.args.get('direction')
    speed_arg = request.args.get('speed')
    print(f'direction: {direction_arg}, speed: {speed_arg}')
    # validate that the arguments are the correct type and in the correct range:
    # if not, return a 400 Bad Request response
    if not direction_arg or not speed_arg:
        return jsonify({'error': 'missing arguments, arguments missing'}), 400
    try:
        direction = float(direction_arg)
        speed = float(speed_arg)
    except ValueError:
        return jsonify({'error': 'invalid arguments, parse error'}), 400
    if direction < -90 or direction > 90 or speed < -1 or speed > 1:
        return jsonify({'error': 'invalid arguments, range error'}), 400

    motion_data = steering.compute_steering(speed, direction)
    print(
        f'servos: FrL: {motion_data["servo_front_left"]} FrR: {motion_data["servo_front_right"]} BaL: {motion_data["servo_back_left"]} BaR: {motion_data["servo_back_right"]}')
    # print('motion_data:')
    # print(motion_data)
    hardware.set_motion_data(motion_data)

    return Response(status=200)

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
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        print('Resetting hardware...')
        hardware.reset()
