# 🏥 Healthcare Chatbot

A comprehensive healthcare chatbot application with support for text and voice. Built with Python and Streamlit for an intuitive web interface.

## ✨ Features

- **💬 Text Chat**: Natural language conversations about health topics
- **🔌 Backend API Integration**: Connects to your AI backend at `http://127.0.0.1:5000/ask`
- **🎤 Voice Input**: Upload and process audio files (speech-to-text ready)
- **🔒 Privacy-Focused**: Secure processing with no permanent data storage
- **🌟 User-Friendly**: Modern, responsive web interface
- **⚡ Fast Processing**: Efficient audio processing
- **📱 Mobile-Friendly**: Responsive design for all device types
- **🛡️ Fallback Mode**: Automatic fallback to local responses if backend is unavailable

## 🚀 Quick Start

### Option 1: Docker (Quickest & Easiest)

**Prerequisites**: Docker and Docker Compose installed

```bash
# Start the application
docker-compose up -d

# Open browser to http://localhost:8501
```

That's it! The chatbot is now running in a container.

### Option 2: Python Installation

**Prerequisites**:
- Python 3.8 or higher
- pip (Python package installer)
- Web browser (Chrome, Firefox, Safari, etc.)

### Installation

1. **Clone or Download the Repository**
   ```bash
   git clone <repository-url>
   cd karim-rayen_healthcarechatbot
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv chatbot_env
   
   # Activate virtual environment
   # On Windows:
   chatbot_env\Scripts\activate
   
   # On macOS/Linux:
   source chatbot_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Install minimal requirements (recommended for testing)
   pip install -r requirements-minimal.txt
   
   # OR install full requirements (for advanced features)
   pip install -r requirements.txt
   ```

4. **Configure Backend API** (Optional)
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and set your backend URL
   # BACKEND_URL=http://127.0.0.1:5000
   ```
   
   See [API_INTEGRATION.md](API_INTEGRATION.md) for detailed API setup.

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Open in Browser**
   The application will automatically open in your default browser at:
   `http://localhost:8501`

## � Backend API Integration

This app connects to a backend API for generating intelligent responses. 

**API Endpoint:** `http://127.0.0.1:5000/ask`

### Quick Setup:
1. Make sure your backend API is running
2. The app will automatically connect and use it
3. If backend is unavailable, app uses local fallback responses

For detailed API integration guide, see [API_INTEGRATION.md](API_INTEGRATION.md).

## �📖 How to Use

### Text Chat
- Simply type your health-related questions in the chat input
- Ask about symptoms, medications, or general health topics
- The chatbot provides informative responses with appropriate disclaimers

### Voice Input
- Click on the "🎤 Voice" tab
- Upload audio files in supported formats (WAV, MP3, M4A)
- The system will transcribe your speech and respond to your query

### Sample Questions
- "What should I know about high blood pressure?"
- "Can you explain my lab results?"
- "What are the side effects of this medication?"
- "How can I improve my sleep quality?"

## 🏗️ Project Structure

```
karim-rayen_healthcarechatbot/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies (full)
├── requirements-minimal.txt    # Essential dependencies only
├── README.md                  # This file
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── chatbot_engine.py      # Core chatbot logic
│   ├── audio_processor.py     # Audio/speech processing
│   └── ui_components.py       # UI components and styling
└── static/                    # Static files
    └── styles.css             # Custom CSS styling
```

## ⚙️ Configuration

The application uses `config.py` for various settings:

- **File Upload Limits**: Configurable size limits for different file types
- **UI Themes**: Customizable colors and styling
- **Feature Flags**: Enable/disable specific features
- **Security Settings**: Privacy and security configurations

### Environment Variables

You can customize the application by setting environment variables:

```bash
# Optional: Set custom colors
export PRIMARY_COLOR="#1E88E5"

# Optional: Set maximum file sizes (in MB)
export MAX_FILE_SIZE_MB=10

# Optional: Set environment mode
export ENVIRONMENT=production
```

## 🔧 Advanced Setup

### Enable Real Speech-to-Text

To enable real speech-to-text functionality:

1. **Install additional dependencies**:
   ```bash
   pip install openai-whisper speechrecognition pyaudio
   ```

2. **For OpenAI Whisper (Recommended)**:
   ```python
   # Add to audio_processor.py
   import whisper
   model = whisper.load_model("base")
   ```

3. **For Google Speech-to-Text**:
   ```bash
   pip install google-cloud-speech
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
   ```

### Production Deployment

For production deployment:

1. **Set environment variables**:
   ```bash
   export ENVIRONMENT=production
   export STREAMLIT_SERVER_PORT=8501
   export STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

2. **Deploy with Docker** (recommended):
   
   **Option A: Using Docker directly**
   ```bash
   # Build Docker image
   docker build -t healthcare-chatbot .
   
   # Run container
   docker run -d -p 8501:8501 --name healthcare-chatbot healthcare-chatbot
   
   # View logs
   docker logs -f healthcare-chatbot
   
   # Stop container
   docker stop healthcare-chatbot
   ```
   
   **Option B: Using Docker Compose** (easiest)
   ```bash
   # Start the application
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop the application
   docker-compose down
   ```
   
   Access the app at `http://localhost:8501`

## 🛡️ Security & Privacy

- **No Permanent Storage**: Conversations are not stored permanently
- **Secure File Processing**: Uploaded files are processed securely and deleted automatically
- **Privacy by Design**: No personal data is shared with third parties
- **Local Processing**: All processing happens locally by default

## ⚠️ Important Disclaimers

- **Medical Disclaimer**: This chatbot provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment.
- **Emergency Situations**: For medical emergencies, contact emergency services immediately (911, 112, or your local emergency number).
- **Professional Consultation**: Always consult qualified healthcare providers for medical concerns and personalized advice.

## 🆘 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r requirements-minimal.txt`

2. **Streamlit not starting**:
   - Check if port 8501 is available
   - Try a different port: `streamlit run app.py --server.port 8502`

3. **File upload errors**:
   - Check file size limits in config.py
   - Ensure supported file formats are used

4. **Audio processing issues**:
   - Install audio dependencies for real speech-to-text
   - Check audio file format compatibility

### Getting Help

1. Check the console for error messages
2. Verify all dependencies are installed correctly
3. Ensure you're using a supported Python version (3.8+)
4. Try with minimal requirements first

## 🔮 Future Enhancements

- **Real-time Voice Recording**: Browser-based voice recording
- **Multi-language Support**: Support for multiple languages
- **Advanced AI Integration**: Integration with medical AI models
- **User Accounts**: Optional user account system
- **Appointment Scheduling**: Integration with healthcare systems
- **Mobile App**: Native mobile application

## 📄 License

This project is provided as-is for educational and demonstration purposes. Please ensure compliance with healthcare regulations and privacy laws in your jurisdiction.

## 🤝 Contributing

Contributions are welcome! Please ensure any medical information is accurate and properly cited. Always include appropriate disclaimers for health-related content.

---

**⚕️ Remember**: This tool is for informational purposes only. Always consult healthcare professionals for medical advice!