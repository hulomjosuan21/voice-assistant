from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

light_states = {
    "living room": "off",
    "bedroom": "off",
    "kitchen": "off",
    "bathroom": "off"
}

@app.route('/toggle-light', methods=['POST'])
def handle_toggle_light():
    try:
        data = request.get_json()
        room = data.get('room')
        switch_to = data.get('switch_to')
        
        if not room or not switch_to:
            return jsonify({"error": "Missing room or switch_to parameter"}), 400
            
        if room not in light_states:
            return jsonify({"error": f"Invalid room. Available rooms: {list(light_states.keys())}"}), 400
            
        if switch_to not in ["on", "off"]:
            return jsonify({"error": "Invalid switch_to value. Must be 'on' or 'off'"}), 400
            
        light_states[room] = switch_to
        logger.info(f"Light state updated - {room}: {switch_to}")
        
        logger.info(f"[WOULD CALL ESP32] Room: {room}, Action: {switch_to}")
        
        return jsonify({
            "status": "success",
            "room": room,
            "state": switch_to,
            "message": f"The light in the {room} is now {switch_to}."
        })
    
    except Exception as e:
        logger.error(f"Error in toggle-light: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/light-status', methods=['GET'])
def get_light_status():
    room = request.args.get('room')
    if room:
        if room in light_states:
            return jsonify({"room": room, "state": light_states[room]})
        return jsonify({"error": "Room not found"}), 404
    return jsonify(light_states)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')