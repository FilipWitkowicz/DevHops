from flask import Flask, send_from_directory, jsonify
import os


app = Flask(__name__)

@app.route('/api/hello')
def api_hello():
    return jsonify({"message": "Nomc, backend działa!"})

if __name__ == '__main__':
    app.run()