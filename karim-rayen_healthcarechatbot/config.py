"""
Configuration file for Healthcare Chatbot
Contains application settings and configurations
"""

import os
from pathlib import Path

# Application Configuration
APP_CONFIG = {
    "name": "Healthcare Chatbot",
    "version": "1.0.0",
    "description": "Intelligent healthcare assistant with multi-modal support",
    "author": "Healthcare Chatbot Team",
    "debug": False
}

# UI Configuration
UI_CONFIG = {
    "theme": "light",
    "primary_color": "#1E88E5", 
    "secondary_color": "#FFC107",
    "success_color": "#4CAF50",
    "error_color": "#F44336",
    "warning_color": "#FF9800",
    "info_color": "#2196F3",
    "background_color": "#F5F5F5",
    "sidebar_width": 350,
    "chat_container_height": 600
}

# File Upload Configuration
UPLOAD_CONFIG = {
    "max_file_size_mb": {
        "audio": 25,  # 25MB for audio files
    },
    "supported_formats": {
        "audio": ["wav", "mp3", "m4a", "mp4", "mpeg", "mpga", "webm"],
    },
    "upload_directory": "temp_uploads"
}

# Chatbot Configuration
CHATBOT_CONFIG = {
    "max_conversation_history": 50,
    "context_window": 5,
    "response_timeout": 30,
    "enable_conversation_export": True,
    "enable_voice_input": True
}

# Audio Processing Configuration
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_size": 1024,
    "format": "wav",
    "transcription_service": "placeholder",  # Options: whisper, google, azure, aws
    "api_keys": {
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_SPEECH_API_KEY"),
        "azure": os.getenv("AZURE_SPEECH_KEY"),
        "aws": os.getenv("AWS_ACCESS_KEY")
    }
}

# Security Configuration
SECURITY_CONFIG = {
    "encrypt_uploads": True,
    "auto_delete_uploads": True,
    "upload_retention_hours": 24,
    "sanitize_inputs": True,
    "rate_limiting": {
        "enabled": True,
        "requests_per_minute": 30,
        "requests_per_hour": 200
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "healthcare_chatbot.log",
    "max_size": "10MB",
    "backup_count": 5,
    "log_conversations": False,  # For privacy
    "log_uploads": True
}

# Health Information Configuration
HEALTH_CONFIG = {
    "emergency_keywords": [
        "emergency", "urgent", "severe pain", "can't breathe", "chest pain",
        "heart attack", "stroke", "bleeding", "unconscious", "overdose",
        "suicide", "self harm", "allergic reaction", "choking"
    ],
    "disclaimer_text": """
    **Medical Disclaimer**: This chatbot provides general health information only and is not a substitute 
    for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers 
    for medical concerns. In case of emergency, contact emergency services immediately.
    """,
    "privacy_text": """
    **Privacy Notice**: Your conversations are processed securely and are not stored permanently. 
    No personal health information is shared with third parties.
    """
}

# API Configuration
API_CONFIG = {
    "enabled": True,
    "backend_url": os.getenv("BACKEND_URL", "http://ml-healthcare-api:5000"),
    "ask_endpoint": "/ask",
    "timeout": 30,
    "host": "localhost",
    "port": 5000,
    "cors_origins": ["*"],
    "rate_limit_per_minute": 60,
    "authentication_required": False
}

# Development Configuration
DEV_CONFIG = {
    "reload_on_change": True,
    "show_debug_info": False,
    "mock_responses": True,  # Use mock responses for testing
    "log_level": "DEBUG",
    "enable_profiling": False
}

# Production Configuration
PROD_CONFIG = {
    "reload_on_change": False,
    "show_debug_info": False,
    "mock_responses": False,
    "log_level": "INFO",
    "enable_profiling": True,
    "use_cdn": True,
    "cache_static_assets": True
}

# Feature Flags
FEATURES = {
    "text_chat": True,
    "voice_input": True,
    "conversation_export": True,
    "real_time_recording": False,  # Coming soon
    "multi_language": False,  # Coming soon
    "integration_apis": False,  # Coming soon
    "user_accounts": False,  # Coming soon
    "conversation_history": True,
    "analytics": False
}

# Helper Functions
def get_config():
    """Get the complete configuration dictionary"""
    return {
        "app": APP_CONFIG,
        "ui": UI_CONFIG,
        "upload": UPLOAD_CONFIG,
        "chatbot": CHATBOT_CONFIG,
        "audio": AUDIO_CONFIG,
        "security": SECURITY_CONFIG,
        "logging": LOGGING_CONFIG,
        "health": HEALTH_CONFIG,
        "api": API_CONFIG,
        "dev": DEV_CONFIG,
        "prod": PROD_CONFIG,
        "features": FEATURES
    }

def get_environment():
    """Get current environment (development/production)"""
    return os.getenv("ENVIRONMENT", "development").lower()

def is_development():
    """Check if running in development mode"""
    return get_environment() == "development"

def is_production():
    """Check if running in production mode"""
    return get_environment() == "production"

def get_upload_path():
    """Get the upload directory path"""
    upload_dir = Path(UPLOAD_CONFIG["upload_directory"])
    upload_dir.mkdir(exist_ok=True)
    return upload_dir

def get_log_path():
    """Get the log file path"""
    return Path(LOGGING_CONFIG["file"])

# Environment-specific configuration loading
def load_environment_config():
    """Load configuration based on current environment"""
    env = get_environment()
    
    if env == "production":
        # Override development settings with production settings
        APP_CONFIG.update(PROD_CONFIG)
        LOGGING_CONFIG["level"] = PROD_CONFIG["log_level"]
    else:
        # Use development settings
        APP_CONFIG.update(DEV_CONFIG)
        LOGGING_CONFIG["level"] = DEV_CONFIG["log_level"]
    
    # Load environment variables if available
    if os.getenv("PRIMARY_COLOR"):
        UI_CONFIG["primary_color"] = os.getenv("PRIMARY_COLOR")
    
    if os.getenv("MAX_FILE_SIZE_MB"):
        for file_type in UPLOAD_CONFIG["max_file_size_mb"]:
            UPLOAD_CONFIG["max_file_size_mb"][file_type] = int(os.getenv("MAX_FILE_SIZE_MB", "10"))

# Initialize configuration on import
load_environment_config()

# Export commonly used configurations
__all__ = [
    "APP_CONFIG", "UI_CONFIG", "UPLOAD_CONFIG", "CHATBOT_CONFIG",
    "AUDIO_CONFIG", "SECURITY_CONFIG", 
    "LOGGING_CONFIG", "HEALTH_CONFIG", "FEATURES",
    "get_config", "get_environment", "is_development", "is_production",
    "get_upload_path", "get_log_path"
]