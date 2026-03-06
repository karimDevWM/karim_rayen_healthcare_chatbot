import pytest
from unittest.mock import MagicMock
from src.audio_processor import AudioProcessor


class TestAudioProcessor:

    def setup_method(self):
        self.processor = AudioProcessor()

    def test_validate_audio_file_none(self):
        is_valid, msg = self.processor.validate_audio_file(None)
        assert is_valid is False

    def test_validate_audio_file_unsupported_format(self):
        mock_file = MagicMock()
        mock_file.name = "audio.xyz"
        mock_file.size = 1024
        is_valid, msg = self.processor.validate_audio_file(mock_file)
        assert is_valid is False
        assert "Unsupported" in msg

    def test_validate_audio_file_too_large(self):
        mock_file = MagicMock()
        mock_file.name = "audio.wav"
        mock_file.size = 30 * 1024 * 1024  # 30MB
        is_valid, msg = self.processor.validate_audio_file(mock_file)
        assert is_valid is False
        assert "large" in msg.lower()

    def test_validate_audio_file_valid(self):
        mock_file = MagicMock()
        mock_file.name = "audio.wav"
        mock_file.size = 1024
        is_valid, msg = self.processor.validate_audio_file(mock_file)
        assert is_valid is True

    def test_transcribe_audio_none(self):
        result = self.processor.transcribe_audio(None)
        assert result is None

    def test_get_audio_info_none(self):
        result = self.processor.get_audio_info(None)
        assert result == {}