from flask import Flask, request, jsonify
import os
from crew import run_my_crew # This links to Step 3

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    topic = data.get('topic')
    
    if topic:
        # This starts the CrewAI process in the background
        run_my_crew(topic) 
        return jsonify({"status": "success", "message": "Crew started"}), 200
    return jsonify({"status": "failed"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
