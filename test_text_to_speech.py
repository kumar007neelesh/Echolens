# test_text_to_speech.py
import pytest
from text2speech import text_to_speech
import os

def test_text_to_speech():
    result_path = text_to_speech("hello", "test_output.mp3")
    assert os.path.exists(result_path)
    os.remove(result_path)  # Clean up after test

