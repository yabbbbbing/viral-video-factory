import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# This is the secret link to your specific CrewAI Cloud setup
# You get this from your CrewAI Dashboard under 'Kickoff' or 'API'
CREW_KICKOFF_URL = "https://api.crewai.com/v1/kickoff" # Standard CrewAI Cloud URL
CREW_ID = "YOUR_CREW_ID_HERE"  # Replace with your actual Crew ID from the dashboard

@app.route('/webhook', methods=['POST'])
def handle_google_sheets():
    # 1. Get the topic from your Google Sheet
    data = request.json
    topic = data.get('topic', 'No topic provided')
    
    print(f"📥 Received topic from Sheets: {topic}")

    # 2. Prepare the payload for CrewAI Cloud
    # We send the 'topic' variable to your Cloud Agents
    payload = {
        "crew_id": CREW_ID,
        "inputs": {"topic": topic}
    }

    # 3. Add your Bearer Token for authorization
    # We will set 'CREWAI_API_KEY' in your Koyeb environment variables later
    headers = {
        "Authorization": f"Bearer {os.getenv('CREWAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        # 4. Trigger the CrewAI Cloud "Kickoff"
        response = requests.post(CREW_KICKOFF_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"🚀 CrewAI Cloud Triggered! Job ID: {result.get('kickoff_id')}")
        
        return jsonify({
            "status": "success",
            "message": "Agents are now working on your viral content!",
            "kickoff_id": result.get('kickoff_id')
        }), 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# This is for Koyeb/Gunicorn to run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
