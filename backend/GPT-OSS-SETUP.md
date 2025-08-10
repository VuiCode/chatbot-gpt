# GPT-OSS-20B Self-Hosted Setup Guide (LM Studio)

This guide helps you set up GPT-OSS-20B as a self-hosted model using LM Studio for your chatbot.

## 📁 File Structure
```
backend/
├── app.py          # Original OpenAI API version (port 5000)
├── appOSS.py       # Self-hosted GPT-OSS-20B version (port 5001)
├── .env            # Configuration for both versions
└── requirements.txt
```

## 🚀 Using LM Studio Setup

### Step 1: Download and Install LM Studio
1. **Visit**: https://lmstudio.ai/
2. **Download** the Windows version
3. **Install** LM Studio on your computer

### Step 2: Download GPT-OSS-20B Model
1. **Open LM Studio**
2. **Go to "Discover" tab** (🔍 icon)
3. **Search for**: `gpt-oss-20b`
4. **Choose one of these models**:
   - `openai/gpt-oss-20b` (main version)
   - `unsloth/gpt-oss-20b-GGUF` (optimized)
   - `ggml-org/gpt-oss-20b-GGUF` (alternative)
5. **Click "Download"** - This will take time (10-40GB model)

### Step 3: Load and Start the Model Server
1. **Go to "Chat" tab** in LM Studio
2. **Select your downloaded GPT-OSS-20B model**
3. **Load the model** (this may take a few minutes)
4. **Go to "Local Server" tab** (🌐 icon)
5. **Make sure the model is selected**
6. **Start the server** - it will run on `http://localhost:1234`
7. **Keep LM Studio running** while using your chatbot

## ⚙️ Configuration

Your `.env` file is already configured for LM Studio:
```env
# Self-hosted GPT-OSS-20B Model Configuration (for appOSS.py)
# LM Studio typically runs on port 1234
MODEL_URL=http://localhost:1234/v1/chat/completions
MODEL_NAME=gpt-oss-20b
```

✅ **No changes needed!** Your configuration is ready for LM Studio.

## 🏃‍♂️ Running Your Chatbot

### Step 1: Start LM Studio Server
1. **Open LM Studio**
2. **Go to "Local Server" tab**
3. **Make sure GPT-OSS-20B is loaded**
4. **Click "Start Server"**
5. **Verify it shows**: `Server running on http://localhost:1234`

### Step 2: Start Your Flask Backend
```bash
cd backend
# Activate virtual environment
chatbot_env\Scripts\activate
# Start the self-hosted version
python appOSS.py
```
Your backend will run on `http://localhost:5001`

### Step 3: Start Your React Frontend
```bash
cd frontend
npm start
```
Your frontend will run on `http://localhost:3000`

## 🔧 Frontend Configuration

Your frontend is already configured to work with the self-hosted version on port 5001.

**No changes needed!** Your `Chatbot.js` should already point to:
```javascript
const res = await axios.post("http://localhost:5001/chat", { message: text });
```

## 🩺 Testing Your Setup

### Test 1: Check LM Studio Server
Open your browser and go to: `http://localhost:1234`
You should see the LM Studio API interface.

### Test 2: Check Flask Backend Health
```bash
curl http://localhost:5001/health
```
Should return: `{"status": "healthy", "model": "gpt-oss-20b"}`

### Test 3: Test Chat Endpoint
```bash
curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello!\"}"
```
Should return a response from GPT-OSS-20B.

### Test 4: Test Full Application
1. Open `http://localhost:3000` in your browser
2. Type a message in the chat
3. You should get a response from your self-hosted GPT-OSS-20B model!

## 🐛 Troubleshooting

### Issue: "Cannot connect to model server"
**Solution**: 
1. Make sure LM Studio is open
2. Check that the Local Server is started
3. Verify the server shows `http://localhost:1234`

### Issue: "Model endpoint not found"
**Solution**:
1. In LM Studio, go to "Local Server" tab
2. Make sure GPT-OSS-20B model is selected
3. Restart the server if needed

### Issue: "Model server timeout"
**Solution**:
1. The model might be loading - wait a few moments
2. Check if your computer has enough RAM (20B model needs ~20GB)
3. Try a smaller model if you have hardware limitations

### Issue: Flask backend won't start
**Solution**:
1. Make sure you're in the `backend` directory
2. Activate virtual environment: `chatbot_env\Scripts\activate`
3. Install requirements: `pip install -r requirements.txt`

## � Performance Tips

1. **GPU Acceleration**: LM Studio will automatically use your GPU if available
2. **Memory Management**: Close other applications to free up RAM
3. **Model Size**: If GPT-OSS-20B is too large, try smaller models like 7B or 13B versions
4. **Quantization**: Choose GGUF models for better performance on consumer hardware

## 🔄 Switching Back to OpenAI

If you want to use OpenAI instead:
1. **Update your frontend** to point to port 5000:
   ```javascript
   const res = await axios.post("http://localhost:5000/chat", { message: text });
   ```
2. **Run the original backend**:
   ```bash
   python app.py  # instead of appOSS.py
   ```
3. **Make sure you have** `OPENAI_API_KEY` in your `.env` file

## ✅ Quick Start Checklist

- [ ] Download and install LM Studio
- [ ] Download GPT-OSS-20B model in LM Studio
- [ ] Load model and start Local Server (port 1234)
- [ ] Your `.env` file points to `http://localhost:1234`
- [ ] Start Flask backend: `python appOSS.py`
- [ ] Start React frontend: `npm start`
- [ ] Test chat at `http://localhost:3000`
