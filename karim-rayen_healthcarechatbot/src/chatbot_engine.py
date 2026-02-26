"""
Healthcare Chatbot Engine
Main chatbot logic and response generation
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import random
import requests
import streamlit as st


class HealthcareChatbot:
    """Main chatbot engine for healthcare conversations"""
    
    def __init__(self, use_api: bool = True):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_context = []
        self.use_api = use_api
        self.api_url = None
        
        # Load API configuration
        if self.use_api:
            try:
                from config import API_CONFIG
                backend_url = API_CONFIG.get("backend_url", "http://ml-healthcare-api:5000")
                ask_endpoint = API_CONFIG.get("ask_endpoint", "/ask")
                self.api_url = f"{backend_url}{ask_endpoint}"
                self.api_timeout = API_CONFIG.get("timeout", 30)
                print(f"✅ API configured: {self.api_url}")
            except Exception as e:
                st.warning(f"Failed to load API config: {e}. Using fallback mode.")
                self.use_api = False
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load healthcare knowledge base"""
        return {
            "greetings": [
                "Hello! I'm your healthcare assistant. How can I help you today?",
                "Hi there! I'm here to help with your healthcare questions.",
                "Welcome! I'm your virtual healthcare companion. What can I assist you with?"
            ],
            "symptoms": {
                "fever": {
                    "info": "Fever is a temporary increase in body temperature, often due to an illness.",
                    "advice": "Rest, stay hydrated, and consider taking fever reducers if recommended by a doctor.",
                    "when_to_seek_help": "Seek medical attention if fever exceeds 103°F (39.4°C) or persists for more than 3 days."
                },
                "headache": {
                    "info": "Headaches can be caused by stress, dehydration, lack of sleep, or underlying conditions.",
                    "advice": "Try rest, hydration, and over-the-counter pain relievers if appropriate.",
                    "when_to_seek_help": "Seek immediate care for sudden severe headaches, vision changes, or neck stiffness."
                },
                "cough": {
                    "info": "Coughs can be dry or productive and may indicate respiratory infections or allergies.",
                    "advice": "Stay hydrated, use honey for soothing, and avoid irritants.",
                    "when_to_seek_help": "See a doctor if cough persists over 3 weeks, contains blood, or causes breathing difficulty."
                }
            },
            "general_health": {
                "exercise": "Regular exercise improves cardiovascular health, strengthens muscles, and boosts mental well-being.",
                "diet": "A balanced diet rich in fruits, vegetables, lean proteins, and whole grains supports overall health.",
                "sleep": "Adults should aim for 7-9 hours of quality sleep per night for optimal health.",
                "hydration": "Drink at least 8 glasses of water daily to maintain proper hydration."
            },
            "emergency_keywords": [
                "emergency", "urgent", "severe pain", "can't breathe", "chest pain", 
                "heart attack", "stroke", "bleeding", "unconscious"
            ]
        }
    
    def generate_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Generate appropriate response based on user input"""
        user_input_lower = user_input.lower()
        
        # Check for emergency indicators first (always use local check)
        if self._is_emergency(user_input_lower):
            return self._handle_emergency()
        
        # Try to get response from API if enabled
        if self.use_api and self.api_url:
            api_response = self._get_api_response(user_input, conversation_history)
            if api_response:
                return api_response
        
        # Fallback to local responses if API is disabled or fails
        # Check for greetings
        if self._is_greeting(user_input_lower):
            return random.choice(self.knowledge_base["greetings"])
        
        # Check for symptom inquiries
        symptom_response = self._check_symptoms(user_input_lower)
        if symptom_response:
            return symptom_response
        
        # Check for general health topics
        health_response = self._check_general_health(user_input_lower)
        if health_response:
            return health_response
        
        # # Document-related queries
        # if "document" in user_input_lower or "file" in user_input_lower:
        #     return self._handle_document_query(user_input)
        
        # Default response with healthcare context
        return self._generate_default_response(user_input)
    
    def _get_api_response(self, user_input: str, conversation_history: List[Dict]) -> Optional[str]:
        """Get response from backend API"""
        try:
            # Prepare request payload
            payload = {
                "message": user_input
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.api_timeout,
                headers={"Content-Type": "application/json"}
            )
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                # Handle different response formats
                if isinstance(data, dict):
                    return data.get("answer") or data.get("response") or data.get("message")
                elif isinstance(data, str):
                    return data
            else:
                st.warning(f"API returned status code {response.status_code}. Using fallback responses.")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend API. Using local fallback responses.")
            self.use_api = False  # Disable API for this session
            return None
        except requests.exceptions.Timeout:
            st.warning("⏱️ API request timed out. Using fallback responses.")
            return None
        except Exception as e:
            st.warning(f"API error: {str(e)}. Using fallback responses.")
            return None
    
    def _is_emergency(self, text: str) -> bool:
        """Check if input indicates a medical emergency"""
        return any(keyword in text for keyword in self.knowledge_base["emergency_keywords"])
    
    def _handle_emergency(self) -> str:
        """Handle emergency situations"""
        return (
            "🚨 **MEDICAL EMERGENCY DETECTED** 🚨\n\n"
            "If this is a life-threatening emergency:\n"
            "• **Call emergency services immediately (911, 112, or your local emergency number)**\n"
            "• Don't wait for online advice\n\n"
            "For urgent but non-life-threatening situations:\n"
            "• Contact your doctor's emergency line\n"
            "• Visit your nearest emergency room\n"
            "• Call a medical helpline\n\n"
            "I'm here to provide general information, but emergency situations require immediate professional medical attention."
        )
    
    def _is_greeting(self, text: str) -> bool:
        """Check if input is a greeting"""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        return any(greeting in text for greeting in greetings)
    
    def _check_symptoms(self, text: str) -> str:
        """Check for symptom-related queries"""
        for symptom, info in self.knowledge_base["symptoms"].items():
            if symptom in text:
                response = f"**About {symptom.title()}:**\n\n"
                response += f"ℹ️ **Information:** {info['info']}\n\n"
                response += f"💡 **General Advice:** {info['advice']}\n\n"
                response += f"⚠️ **When to Seek Help:** {info['when_to_seek_help']}\n\n"
                response += "**Disclaimer:** This is general information only. Please consult a healthcare professional for personalized medical advice."
                return response
        return ""
    
    def _check_general_health(self, text: str) -> str:
        """Check for general health topics"""
        for topic, info in self.knowledge_base["general_health"].items():
            if topic in text:
                return f"**About {topic.title()}:**\n\n{info}\n\n*Remember: This is general guidance. Consult healthcare professionals for personalized advice.*"
        return ""
    
    def _handle_document_query(self, user_input: str) -> str:
        """Handle document-related queries"""
        if "analyze" in user_input.lower() or "review" in user_input.lower():
            return (
                "I can help analyze your uploaded documents! Here's what I can do:\n\n"
                "📋 **Medical Reports:** Extract key findings and explain medical terms\n"
                "💊 **Prescriptions:** Review medication information and dosages\n"
                "📊 **Lab Results:** Help interpret common test results\n"
                "📝 **Health Records:** Organize and summarize medical history\n\n"
                "Please upload your document and ask specific questions about it!"
            )
        
        return (
            "I see you've mentioned a document. I can help you:\n\n"
            "• Extract and summarize key medical information\n"
            "• Explain medical terminology\n"
            "• Answer questions about the content\n\n"
            "Please upload your document using the Document tab above!"
        )
    
    def _generate_default_response(self, user_input: str) -> str:
        """Generate a default helpful response"""
        responses = [
            "I understand you're asking about healthcare. While I can provide general information, I always recommend consulting with qualified healthcare professionals for specific medical advice.",
            "That's an interesting health-related question. I can offer general guidance, but please remember that individual health needs vary. Consider speaking with a healthcare provider for personalized advice.",
            "I'm here to help with general health information! For specific medical concerns, it's always best to consult with healthcare professionals who can provide personalized care."
        ]
        
        base_response = random.choice(responses)
        
        # Add contextual suggestions
        suggestions = (
            "\n\n**I can help you with:**\n"
            "• General health and wellness information\n"
            "• Understanding common symptoms\n"
            "• Analyzing uploaded medical documents\n"
            "• Answering questions about health topics\n\n"
            "**For urgent matters:** Always contact healthcare professionals directly!"
        )
        
        return base_response + suggestions


class ConversationManager:
    """Manage conversation context and history"""
    
    def __init__(self):
        self.context_window = 5  # Number of previous messages to consider
    
    def get_relevant_context(self, conversation_history: List[Dict], current_input: str) -> str:
        """Extract relevant context from conversation history"""
        if len(conversation_history) == 0:
            return ""
        
        # Get recent messages
        recent_messages = conversation_history[-self.context_window:]
        
        context_summary = "Recent conversation context:\n"
        for msg in recent_messages:
            if msg["role"] == "user":
                context_summary += f"User asked: {msg['content'][:100]}...\n"
        
        return context_summary
    
    def should_reference_document(self, conversation_history: List[Dict]) -> bool:
        """Check if we should reference uploaded documents in response"""
        # Check if any recent messages mention documents
        recent_messages = conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history
        
        for msg in recent_messages:
            if msg.get("type") == "document" or "document" in msg.get("content", "").lower():
                return True
        
        return False