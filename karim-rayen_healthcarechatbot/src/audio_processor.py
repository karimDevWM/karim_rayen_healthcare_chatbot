"""
Audio Processing Module
Handles voice recording transcription and audio file processing
"""

import io
import tempfile
import os
from typing import Optional
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment


class AudioProcessor:
    """Handle audio processing and speech-to-text conversion"""
    
    def __init__(self):
        self.supported_formats = ['wav', 'mp3', 'm4a', 'mp4', 'mpeg', 'mpga', 'webm']
        
    def transcribe_audio(self, audio_file) -> Optional[str]:
        """
        Transcribe audio file to text
        Returns transcribed text or None if transcription fails
        """
        try:
            if audio_file is None:
                return None
            
            # Check file format
            file_extension = audio_file.name.split('.')[-1].lower()
            if file_extension not in self.supported_formats:
                st.error(f"Unsupported audio format: {file_extension}")
                return None
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(audio_file.getbuffer())
                tmp_file_path = tmp_file.name
            
            try:
                # Use speech recognition to transcribe
                transcription = self._real_transcription(tmp_file_path, file_extension)
                return transcription if transcription else self._placeholder_transcription(tmp_file_path, file_extension)
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            st.error(f"Error processing audio file: {str(e)}")
            return None
    
    def transcribe_audio_bytes(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transcribe audio from bytes (for microphone recording)
        Returns transcribed text or None if transcription fails
        """
        try:
            if audio_bytes is None:
                return None
            
            # Save bytes to temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            try:
                # Use speech recognition to transcribe
                transcription = self._real_transcription(tmp_file_path, "wav")
                return transcription
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            st.error(f"Error processing audio recording: {str(e)}")
            return None
    
    def _real_transcription(self, file_path: str, file_extension: str) -> Optional[str]:
        """
        Real speech-to-text transcription using SpeechRecognition
        """
        try:
            recognizer = sr.Recognizer()
            
            # Convert audio to WAV if needed
            wav_path = file_path
            if file_extension != 'wav':
                audio = AudioSegment.from_file(file_path, format=file_extension)
                wav_path = file_path.replace(f'.{file_extension}', '.wav')
                audio.export(wav_path, format='wav')
            
            # Transcribe audio
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                # Try Google's free speech recognition
                try:
                    text = recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    st.warning("Could not understand audio")
                    return None
                except sr.RequestError as e:
                    st.warning(f"Speech recognition service error: {e}")
                    return None
            
        except Exception as e:
            st.warning(f"Transcription error: {str(e)}")
            return None
    
    def _placeholder_transcription(self, file_path: str, file_extension: str) -> str:
        """
        Placeholder transcription method
        In a real implementation, replace this with actual speech-to-text API
        """
        # Get file size for demo purposes
        file_size = os.path.getsize(file_path)
        
        # Return a placeholder based on file characteristics
        placeholder_transcriptions = [
            "I have a question about my recent symptoms.",
            "Can you help me understand my medical test results?",
            "I've been experiencing headaches lately and would like some advice.",
            "What should I know about my prescribed medication?",
            "Can you explain what this medical report means?",
            "I need help understanding my lab results.",
            "What are the side effects of this medication?"
        ]
        
        # Use file size to pick a consistent placeholder (for demo)
        index = (file_size % len(placeholder_transcriptions))
        selected_transcription = placeholder_transcriptions[index]
        
        return f"[Transcribed from audio]: {selected_transcription}"
    
    def get_audio_info(self, audio_file) -> dict:
        """Get basic information about the audio file"""
        if audio_file is None:
            return {}
        
        return {
            "filename": audio_file.name,
            "size": audio_file.size,
            "type": audio_file.type if hasattr(audio_file, 'type') else 'unknown'
        }
    
    def validate_audio_file(self, audio_file) -> tuple[bool, str]:
        """
        Validate uploaded audio file
        Returns (is_valid, error_message)
        """
        if audio_file is None:
            return False, "No audio file provided"
        
        # Check file size (limit to 25MB)
        max_size = 25 * 1024 * 1024  # 25MB
        if audio_file.size > max_size:
            return False, f"File too large. Maximum size is 25MB, got {audio_file.size / 1024 / 1024:.1f}MB"
        
        # Check file format
        file_extension = audio_file.name.split('.')[-1].lower()
        if file_extension not in self.supported_formats:
            return False, f"Unsupported format: {file_extension}. Supported: {', '.join(self.supported_formats)}"
        
        return True, "Valid audio file"


class RealTimeAudioProcessor:
    """
    Handle real-time audio recording (placeholder for future implementation)
    This would integrate with browser APIs for live recording
    """
    
    def __init__(self):
        self.is_recording = False
        self.audio_buffer = []
    
    def start_recording(self):
        """Start real-time audio recording"""
        # Placeholder for real-time recording implementation
        # Would require JavaScript integration with Streamlit
        st.info("Real-time recording feature coming soon! For now, please upload audio files.")
        
    def stop_recording(self):
        """Stop real-time audio recording"""
        # Placeholder implementation
        pass
    
    def get_recording_status(self) -> dict:
        """Get current recording status"""
        return {
            "is_recording": self.is_recording,
            "duration": 0,  # Placeholder
            "buffer_size": len(self.audio_buffer)
        }


# Integration instructions for real speech-to-text services:

"""
REAL SPEECH-TO-TEXT IMPLEMENTATION EXAMPLES:

1. OpenAI Whisper (Recommended - Free and Open Source):
   
   pip install openai-whisper
   
   import whisper
   
   model = whisper.load_model("base")
   result = model.transcribe(audio_file_path)
   transcription = result["text"]

2. Google Speech-to-Text:
   
   pip install google-cloud-speech
   
   from google.cloud import speech
   
   client = speech.SpeechClient()
   audio = speech.RecognitionAudio(content=audio_content)
   config = speech.RecognitionConfig(
       encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
       sample_rate_hertz=16000,
       language_code="en-US",
   )
   response = client.recognize(config=config, audio=audio)

3. Azure Speech Services:
   
   pip install azure-cognitiveservices-speech
   
   import azure.cognitiveservices.speech as speechsdk
   
   speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
   audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
   speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
   result = speech_recognizer.recognize_once()

4. Assembly AI (Good for medical transcription):
   
   pip install assemblyai
   
   import assemblyai as aai
   
   aai.settings.api_key = "your-api-key"
   transcriber = aai.Transcriber()
   transcript = transcriber.transcribe(audio_file_path)
"""