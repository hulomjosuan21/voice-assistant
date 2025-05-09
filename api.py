from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')