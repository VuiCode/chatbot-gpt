import os                          # OS access for environment variables
from dotenv import load_dotenv     # Load secrets from a local .env file
from flask import Flask, request, jsonify  # Web server + request/response helpers
from flask_cors import CORS        # Enable CORS so a frontend on another port can call this API
import requests                    # For making HTTP requests to local model server
import json                        # JSON handling

load_dotenv()                      # Read variables (e.g., MODEL_URL) from .env
app = Flask(__name__)              # Create the Flask application
CORS(app)                          # Allow cross-origin requests (React dev server -> Flask)

# Configuration for self-hosted GPT-OSS-20B model
MODEL_URL = os.getenv("MODEL_URL", "http://localhost:8080/v1/chat/completions")  # Local model server URL
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss-20b")  # Model name

@app.route("/chat", methods=["POST"])                  # Define a POST endpoint at /chat
def chat():
    data = request.get_json(silent=True) or {}        # Parse JSON body safely
    user_message = data.get("message", "").strip()    # Extract and trim the user's message
    if not user_message:                              # Basic validation
        return jsonify({"error": "Empty message"}), 400

    try:
        # Prepare request for self-hosted GPT-OSS-20B model
        payload = {
            "model": MODEL_NAME,                      # Specify which model to use (gpt-oss-20b)
            "messages": [                             # Conversation history array
                {"role": "system", "content": "You are a helpful AI assistant."},  # System prompt to set AI behavior
                {"role": "user", "content": user_message}                          # User's actual message/question
            ],
            "temperature": 0.7,                       # Controls randomness (0.0=deterministic, 1.0=very creative)
            "max_tokens": 512,                        # Maximum number of tokens in the response
            "stream": False,                          # Whether to stream response chunks (False=wait for complete response)
            "top_p": 0.9,                            # Nucleus sampling: consider top 90% probability mass
            "frequency_penalty": 0.0,                 # Reduce repetition of tokens based on frequency (0.0=no penalty)
            "presence_penalty": 0.0                   # Reduce repetition of topics based on presence (0.0=no penalty)
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Make request to self-hosted model
        response = requests.post(
            MODEL_URL,
            json=payload,
            headers=headers,
            timeout=120  # 60 second timeout for large model
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            return jsonify({"reply": reply})
        elif response.status_code == 404:
            return jsonify({"error": "Model endpoint not found. Check MODEL_URL configuration."}), 404
        elif response.status_code == 401:
            return jsonify({"error": "Unauthorized. Check API key configuration."}), 401
        else:
            return jsonify({"error": f"Model server error: {response.status_code} - {response.text}"}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to model server. Is GPT-OSS-20B running on the configured port?"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Model server timeout. GPT-OSS-20B is taking too long to respond."}), 504
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response format from model server"}), 502
    except Exception as e:                            # Catch and report runtime errors
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])                # Health check endpoint
def health():
    """Check if the model server is available"""
    try:
        response = requests.get(f"{MODEL_URL.replace('/v1/chat/completions', '/health')}", timeout=5)
        if response.status_code == 200:
            return jsonify({"status": "healthy", "model": MODEL_NAME})
        else:
            return jsonify({"status": "model_server_error", "code": response.status_code}), 503
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "model_server_offline"}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":                            # Run only when executed directly
    print(f"🤖 Starting GPT-OSS-20B Chatbot Server...")
    print(f"📡 Model URL: {MODEL_URL}")
    print(f"🔧 Model Name: {MODEL_NAME}")
    print(f"🚀 Server will run on http://localhost:5001")
    app.run(debug=True, port=5001)                    # Start dev server on http://localhost:5001 (different port)
