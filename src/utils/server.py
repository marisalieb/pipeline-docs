from pathlib import Path
import json
import sys
from flask import Flask, request, jsonify

# code modified from this promt
# prompt: can you create a Flask-based backend to get coordinates from a map
# Copilot suggested this:
# app = Flask(__name__)
# coordinates_store = []
# @app.route('/submit-coordinates', methods=['POST'])
# def submit_coordinates():
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
#     if latitude is None or longitude is None:
#         return jsonify({'error': 'Missing latitude or longitude'}), 400
#     coordinates_store.append({'latitude': latitude, 'longitude': longitude})
#     print(f"Received coordinates: {latitude}, {longitude}")
#     return jsonify({'message': 'Coordinates received successfully'}), 200
# @app.route('/get-coordinates', methods=['GET'])
# def get_coordinates():
#     return jsonify({'coordinates': coordinates_store}), 200



def create_app(data_folder):
    """
    Create and configure the Flask app.

    Args:
        data_folder (str): Path to the data folder.

    Returns:
        Flask app: Configured Flask application.
    """
    Path(data_folder).mkdir(parents=True, exist_ok=True)

    app = Flask(__name__)
    app.config['DATA_FOLDER'] = data_folder

    @app.route('/')
    def index():
        return "Flask is running"

    @app.route('/save-coords', methods=['POST', 'OPTIONS'])
    def save_coords():
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            return response

        data = request.get_json(force=True)

        save_path = Path(app.config['DATA_FOLDER']) / "coords.json"
        print("Saving coords to:", save_path)

        with open(save_path, 'w') as f:
            json.dump(data, f, indent=2)

        response = jsonify({
            "status": "success",
            "message": "Coordinates saved!",
            "path": str(save_path)
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return app


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    data_folder = Path(sys.argv[1])
    if not data_folder.is_dir():
        print(f"Invalid data folder: {data_folder}")
        sys.exit(1)

    app = create_app(data_folder)
    app.run(host='127.0.0.1', port=5001)

