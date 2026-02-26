"""
Healthcare Chatbot Package
A comprehensive chatbot application with multi-modal input support
"""

__version__ = "1.0.0"
__author__ = "Healthcare Chatbot Team"

# Import main components
from .chatbot_engine import HealthcareChatbot, ConversationManager
from .audio_processor import AudioProcessor, RealTimeAudioProcessor
from .ui_components import UIComponents, CustomStreamlitComponents

__all__ = [
    "HealthcareChatbot",
    "ConversationManager", 
    "AudioProcessor",
    "RealTimeAudioProcessor",
    "DocumentProcessor", 
    "UIComponents",
    "CustomStreamlitComponents"
]