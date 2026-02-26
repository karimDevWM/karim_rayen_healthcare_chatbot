"""
UI Components Module
Custom Streamlit components and styling for the healthcare chatbot
"""

import streamlit as st
from datetime import datetime
import base64


class UIComponents:
    """Custom UI components for the healthcare chatbot"""
    
    def __init__(self):
        self.primary_color = "#1E88E5"
        self.secondary_color = "#FFC107"
        self.success_color = "#4CAF50"
        self.error_color = "#F44336"
        self.background_color = "#F5F5F5"
        
    def render_header(self):
        """Render the application header with branding and navigation"""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1E88E5 0%, #1976D2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
        }
        .main-header p {
            color: #E3F2FD;
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        .feature-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.25rem 0.75rem;
            margin: 0.25rem;
            border-radius: 15px;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="main-header">
            <h1>🏥 Healthcare Chat Assistant</h1>
            <p>Your intelligent healthcare companion with multi-modal support</p>
            <div>
                <span class="feature-badge">💬 Text Chat</span>
                <span class="feature-badge">🎤 Voice Input</span>
                <span class="feature-badge">🔒 Secure & Private</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_status_indicator(self, status: str, message: str):
        """Render status indicator with appropriate styling"""
        status_icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "processing": "⏳"
        }
        
        status_colors = {
            "success": self.success_color,
            "error": self.error_color,
            "warning": "#FF9800",
            "info": self.primary_color,
            "processing": "#9C27B0"
        }
        
        icon = status_icons.get(status, "ℹ️")
        color = status_colors.get(status, self.primary_color)
        
        st.markdown(f"""
        <div style="
            background: {color}15;
            border-left: 4px solid {color};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        ">
            <strong style="color: {color};">{icon} {message}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    def render_chat_message(self, message: str, is_user: bool, timestamp: str = None):
        """Render a chat message with appropriate styling"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
        
        if is_user:
            # User message (right-aligned, blue)
            st.markdown(f"""
            <div style="
                background: {self.primary_color};
                color: white;
                padding: 1rem;
                border-radius: 18px 18px 4px 18px;
                margin: 1rem 0 1rem 2rem;
                margin-left: auto;
                max-width: 80%;
            ">
                <div style="margin-bottom: 0.5rem;">{message}</div>
                <div style="font-size: 0.8rem; opacity: 0.8; text-align: right;">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Assistant message (left-aligned, gray)
            st.markdown(f"""
            <div style="
                background: white;
                color: #333;
                padding: 1rem;
                border-radius: 18px 18px 18px 4px;
                margin: 1rem 2rem 1rem 0;
                max-width: 80%;
                border: 1px solid #E0E0E0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="margin-bottom: 0.5rem;">{message}</div>
                <div style="font-size: 0.8rem; opacity: 0.6;">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_file_upload_area(self, upload_type: str):
        """Render custom file upload area"""
        if upload_type == "audio":
            icon = "🎤"
            title = "Audio Upload"
            subtitle = "Upload voice recordings (WAV, MP3, M4A)"
            color = "#FF6B6B"
        elif upload_type == "document":
            icon = "📄"
            title = "Document Upload"
            subtitle = "Upload medical documents (PDF, DOCX, Images)"
            color = "#4ECDC4"
        else:
            icon = "📁"
            title = "File Upload"
            subtitle = "Upload your file"
            color = self.primary_color
        
        st.markdown(f"""
        <div style="
            border: 2px dashed {color};
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background: {color}0A;
            margin: 1rem 0;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="color: {color}; margin-bottom: 0.5rem;">{title}</h3>
            <p style="color: #666; margin: 0;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_feature_card(self, title: str, description: str, icon: str, color: str = None):
        """Render a feature card component"""
        if color is None:
            color = self.primary_color
        
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid {color};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
                <h3 style="color: {color}; margin: 0;">{title}</h3>
            </div>
            <p style="color: #666; margin: 0; line-height: 1.6;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_stats_card(self, label: str, value: str, icon: str = "📊"):
        """Render a statistics card"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {self.primary_color}, {self.primary_color}DD);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
        ">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <h2 style="margin: 0; font-size: 2rem;">{value}</h2>
            <p style="margin: 0; opacity: 0.9;">{label}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_privacy_notice(self):
        """Render privacy and security notice"""
        st.markdown("""
        <div style="
            background: #E8F5E8;
            border: 1px solid #4CAF50;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <h4 style="color: #2E7D32; margin: 0 0 0.5rem 0;">🔒 Privacy & Security</h4>
            <ul style="color: #2E7D32; margin: 0; padding-left: 1.5rem;">
                <li>Your conversations are not stored permanently</li>
                <li>Uploaded documents are processed securely</li>
                <li>No personal data is shared with third parties</li>
                <li>This tool provides general information only</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def render_disclaimer(self):
        """Render medical disclaimer"""
        st.markdown("""
        <div style="
            background: #FFF3E0;
            border: 1px solid #FF9800;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0;">⚠️ Medical Disclaimer</h4>
            <p style="color: #E65100; margin: 0; font-size: 0.9rem; line-height: 1.5;">
                This chatbot provides general health information only and is not a substitute for professional medical advice, 
                diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns. 
                In case of emergency, contact emergency services immediately.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_loading_animation(self, message: str = "Processing..."):
        """Render loading animation"""
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            background: {self.background_color};
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <div style="
                font-size: 2rem;
                animation: spin 1s linear infinite;
                margin-bottom: 1rem;
                display: inline-block;
            ">⏳</div>
            <p style="color: #666; margin: 0;">{message}</p>
        </div>
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """Render quick action buttons"""
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Sample Questions", use_container_width=True):
                return "sample_questions"
        
        with col2:
            if st.button("🏥 Health Tips", use_container_width=True):
                return "health_tips"
        
        with col3:
            if st.button("📚 How to Use", use_container_width=True):
                return "how_to_use"
        
        return None
    
    def render_sample_questions(self):
        """Render sample questions sidebar"""
        st.markdown("### 💡 Sample Questions")
        
        sample_questions = [
            "What should I know about high blood pressure?",
            "Can you explain my lab results?",
            "What are the side effects of this medication?",
            "How can I improve my sleep quality?",
            "What does this medical term mean?",
            "When should I see a doctor for a headache?"
        ]
        
        for question in sample_questions:
            if st.button(f"💬 {question}", use_container_width=True, key=f"sample_{question[:20]}"):
                return question
        
        return None
    
    def render_help_section(self):
        """Render help and instructions section"""
        st.markdown("""
        ### 📖 How to Use
        
        **Text Chat:**
        - Type your health questions in the chat input
        - Ask about symptoms, medications, or general health
        
        **Voice Input:**
        - Upload audio files (WAV, MP3, M4A)
        - Speak clearly for better transcription
        
        **Document Upload:**
        - Upload medical documents (PDF, Word, Images)
        - Ask specific questions about the content
        - Supported formats: PDF, DOCX, PNG, JPG
        
        **Tips for Best Results:**
        - Be specific in your questions
        - Provide context when asking about symptoms
        - Always consult healthcare professionals for serious concerns
        """)


class CustomStreamlitComponents:
    """Additional custom components and utilities"""
    
    @staticmethod
    def create_download_link(data: str, filename: str, text: str):
        """Create a download link for text data"""
        b64 = base64.b64encode(data.encode()).decode()
        return f'<a href="data:text/plain;base64,{b64}" download="{filename}">{text}</a>'
    
    @staticmethod
    def render_progress_bar(percentage: float, label: str = "Progress"):
        """Render a custom progress bar"""
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <p style="margin-bottom: 0.5rem; font-weight: 500;">{label}</p>
            <div style="
                background: #E0E0E0;
                border-radius: 10px;
                height: 20px;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, #4CAF50, #45A049);
                    height: 100%;
                    width: {percentage}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="text-align: right; font-size: 0.9rem; color: #666; margin-top: 0.25rem;">
                {percentage:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)