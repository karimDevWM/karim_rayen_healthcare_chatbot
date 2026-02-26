# 🔌 API Integration Guide

The Healthcare Chatbot now connects to a backend API for generating responses.

## Backend API Endpoint

The app makes POST requests to:
```
http://127.0.0.1:5000/ask
```

## API Request Format

The app sends JSON payloads with the following structure:

```json
{
  "message": "What are the symptoms of flu?"
}
```

### Request Fields:
- **message** (string, required): The user's question or message

## Expected API Response Format

The backend should return JSON in one of these formats:

### Format 1: Object with "answer" field
```json
{
  "answer": "The flu commonly causes fever, cough, sore throat..."
}
```

### Format 2: Object with "response" field
```json
{
  "response": "The flu commonly causes fever, cough, sore throat..."
}
```

### Format 3: Object with "message" field
```json
{
  "message": "The flu commonly causes fever, cough, sore throat..."
}
```

### Format 4: Plain string
```json
"The flu commonly causes fever, cough, sore throat..."
```

## Configuration

### Environment Variables

Set the backend URL using environment variables:

```bash
# .env file
BACKEND_URL=http://127.0.0.1:5000
```

### Config File

Or modify [config.py](config.py):

```python
API_CONFIG = {
    "enabled": True,
    "backend_url": "http://127.0.0.1:5000",
    "ask_endpoint": "/ask",
    "timeout": 30
}
```

## Error Handling

The app has built-in fallback mechanisms:

1. **Connection Error**: If backend is unreachable, uses local fallback responses
2. **Timeout**: If request takes >30 seconds, uses fallback responses  
3. **API Error**: If backend returns error, uses fallback responses
4. **Emergency Detection**: Always handled locally (never sent to API)

## Testing the Integration

### 1. Start Your Backend API

Make sure your backend is running at `http://127.0.0.1:5000`

Test it directly:
```bash
curl -X POST http://127.0.0.1:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a fever?"}'
```

### 2. Start the Chatbot

```bash
# Activate virtual environment
source chatbot_env/bin/activate  # Linux/Mac
# or
chatbot_env\Scripts\activate  # Windows

# Install dependencies (including requests)
pip install -r requirements-minimal.txt

# Run the app
streamlit run app.py
```

### 3. Test API Connection

When you send a message in the chatbot:
- ✅ If backend is available: Response comes from your API
- ⚠️ If backend is unavailable: Warning shown, uses fallback responses

## Docker Deployment

### Docker Compose (Backend on Host)

```bash
# Start the chatbot (connects to backend on host machine)
docker-compose up -d
```

The Docker container uses `host.docker.internal` to reach your backend API running on the host machine.

### Docker Compose (Full Stack)

Create a docker-compose.yml that includes both services:

```yaml
version: '3.8'

services:
  backend:
    image: your-backend-image
    container_name: healthcare-backend
    ports:
      - "5000:5000"
    networks:
      - healthcare-net

  frontend:
    build: .
    container_name: healthcare-chatbot
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:5000
    depends_on:
      - backend
    networks:
      - healthcare-net

networks:
  healthcare-net:
    driver: bridge
```

## Example Backend Implementation

### Flask Example

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    message = data.get('message', '')
    
    # Your AI/ML logic here
    answer = generate_response(message)
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class MessageRequest(BaseModel):
    message: str

@app.post("/ask")
async def ask(request: MessageRequest):
    # Your AI/ML logic here
    answer = generate_response(request.message)
    return {"answer": answer}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

## Monitoring API Calls

Check Streamlit console output for:
- ✅ Successful API connections
- ⚠️ Connection warnings (fallback mode)
- ❌ API errors

## Switching Between API and Local Mode

The chatbot automatically:
1. Tries API first (if enabled)
2. Falls back to local responses if API fails
3. Disables API for session if connection fails

To force local mode:
```python
# In app.py or when initializing
chatbot = HealthcareChatbot(use_api=False)
```

## Security Considerations

1. **HTTPS**: Use HTTPS in production (`https://your-api.com/ask`)
2. **Authentication**: Add API keys if needed:
   ```python
   headers = {
       "Content-Type": "application/json",
       "Authorization": f"Bearer {API_KEY}"
   }
   ```
3. **Rate Limiting**: Backend should implement rate limiting
4. **Input Validation**: Backend should validate and sanitize inputs
5. **CORS**: Configure CORS properly if frontend/backend on different domains

## Troubleshooting

### "Cannot connect to backend API"
- Check if backend is running: `curl http://127.0.0.1:5000/ask`
- Verify firewall settings
- Check BACKEND_URL in environment variables

### "API request timed out"
- Increase timeout in config.py
- Optimize backend response time
- Check network connectivity

### "API returned status code 500"
- Check backend logs for errors
- Verify request payload format
- Test backend endpoint directly

### Docker: "Connection refused"
- Use `host.docker.internal` instead of `127.0.0.1` or `localhost`
- Ensure extra_hosts is configured in docker-compose.yml
- Check if backend is accessible from container

## Next Steps

1. ✅ Backend API is running at `http://127.0.0.1:5000/ask`
2. ✅ Install dependencies: `pip install -r requirements-minimal.txt`
3. ✅ Start chatbot: `streamlit run app.py`
4. ✅ Test conversation with your backend AI!

---

For more information, see [README.md](README.md) and [config.py](config.py).
