"""
Healthcare Chatbot Application
A comprehensive chatbot with support for text, voice
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
import json
from pathlib import Path
from fpdf import FPDF

# Import custom modules
from src.chatbot_engine import HealthcareChatbot
from src.audio_processor import AudioProcessor
from src.ui_components import UIComponents
from audio_recorder_streamlit import audio_recorder

# Configure page
st.set_page_config(
    page_title="Healthcare Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ChatbotApp:
    def __init__(self):
        self.chatbot = HealthcareChatbot()
        self.audio_processor = AudioProcessor()
        self.ui = UIComponents()
        
        # Initialize session state
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
    
    def run(self):
        """Main application runner"""
        self.ui.render_header()
        
        # Create main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_chat_interface()
        
        with col2:
            self.render_sidebar()
    
    def render_chat_interface(self):
        """Render the main chat interface"""
        st.markdown("### 💬 Chat Interface")
        
        # Chat history container
        chat_container = st.container()
        
        # Display conversation history
        self.display_conversation_history(chat_container)
        
        # Input methods tabs
        tab1, tab2 = st.tabs(["📝 Text", "🎤 Voice"])
        
        with tab1:
            self.render_text_input()
        
        with tab2:
            self.render_voice_input()
    
    def render_sidebar(self):
        """Render sidebar with settings and options"""
        st.markdown("### ⚙️ Settings")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()
        
        # Export conversation
        if st.button("💾 Export Chat", use_container_width=True):
            self.export_conversation()
    
    def display_conversation_history(self, container):
        """Display chat conversation history"""
        with container:
            for message in st.session_state.conversation_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
    
    def render_text_input(self):
        """Render text input interface"""
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            self.process_user_input(user_input, "text")
    
    def render_voice_input(self):
        """Render voice input interface"""
        st.markdown("🎤 **Voice Recording**")
        st.info("Click the microphone button to start recording. Speak your question, then click stop.")
        
        # Audio recording component
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="2x",
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            # Process recorded audio
            with st.spinner("Transcribing your speech..."):
                transcript = self.audio_processor.transcribe_audio_bytes(audio_bytes)
            
            if transcript:
                st.success(f"✅ Transcribed: {transcript}")
                if st.button("Send to chatbot", key="send_voice"):
                    self.process_user_input(transcript, "voice")
            else:
                st.error("Could not transcribe audio. Please try again.")
    
    def process_user_input(self, user_input, input_type):
        """Process user input and generate response"""
        # Add user message to conversation
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input,
            "type": input_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate bot response
        with st.spinner("Thinking..."):
            response = self.chatbot.generate_response(
                user_input, 
                st.session_state.conversation_history
            )
        
        # Add bot response to conversation
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Rerun to update the interface
        st.rerun()
    
    def export_conversation(self):
        """Export conversation to PDF"""
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Healthcare Chatbot - Conversation Export', 0, 1, 'C')
        pdf.ln(5)
        
        # Export timestamp
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f'Exported on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        pdf.ln(5)
        
        # Conversation history
        pdf.set_font('Arial', '', 11)
        
        for i, message in enumerate(st.session_state.conversation_history, 1):
            role = "User" if message["role"] == "user" else "Assistant"
            timestamp = message.get("timestamp", "")
            
            # Role and timestamp
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 8, f"{role} - {timestamp[:19] if timestamp else ''}", 0, 1)
            
            # Message content
            pdf.set_font('Arial', '', 10)
            content = message["content"]
            # Handle special characters and encoding
            try:
                pdf.multi_cell(0, 6, content)
            except:
                # Fallback for special characters
                pdf.multi_cell(0, 6, content.encode('latin-1', 'replace').decode('latin-1'))
            
            pdf.ln(3)
        
        # Generate PDF data
        pdf_data = bytes(pdf.output(dest='S'))
        
        st.download_button(
            label="Download Conversation (PDF)",
            data=pdf_data,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

def main():
    """Main function to run the application"""
    app = ChatbotApp()
    app.run()

if __name__ == "__main__":
    main()