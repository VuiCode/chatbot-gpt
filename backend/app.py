


import os                          # OS access for environment variables
from dotenv import load_dotenv     # Load secrets from a local .env file
from flask import Flask, request, jsonify  # Web server + request/response helpers
from flask_cors import CORS        # Enable CORS so a frontend on another port can call this API
from openai import OpenAI          # OpenAI SDK client

load_dotenv()                      # Read variables (e.g., OPENAI_API_KEY) from .env
app = Flask(__name__)              # Create the Flask application
CORS(app)                          # Allow cross-origin requests (React dev server -> Flask)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize OpenAI client with your API key

@app.route("/chat", methods=["POST"])                  # Define a POST endpoint at /chat
def chat():
    data = request.get_json(silent=True) or {}        # Parse JSON body safely
    user_message = data.get("message", "").strip()    # Extract and trim the user's message
    if not user_message:                              # Basic validation
        return jsonify({"error": "Empty message"}), 400

    try:
        completion = client.chat.completions.create(  # Call OpenAI chat completion API
            model="gpt-4o-mini",                      # Choose a fast, low-cost model (change if needed)
            messages=[{"role": "user", "content": user_message}],  # Single-turn message payload
            temperature=0.7                           # Output creativity (0=deterministic, higher=more creative)
        )
        reply = completion.choices[0].message.content # Extract assistant reply text
        return jsonify({"reply": reply})              # Send reply back to the frontend as JSON
    except Exception as e:                            # Catch and report runtime errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":                            # Run only when executed directly
    app.run(debug=True, port=5000)                    # Start dev server on http://localhost:5000
