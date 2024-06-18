from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        code = request.json.get('code', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400

        filename = f'temp_code_{uuid.uuid4().hex}.py'

        with open(filename, 'w') as file:
            file.write(code)

        result = subprocess.run(['python', filename], capture_output=True, text=True)

        os.remove(filename)

        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hello', methods=['GET'])
def run_hello():
    return jsonify({
        'result': "Hello World"
    })
    
@app.route('/runback', methods=['POST'])
def run_back():
    try:
        code = request.json.get('code', '')
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        return jsonify({
            'result': code,
            'working': 'yes'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)