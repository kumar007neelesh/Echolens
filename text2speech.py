# text2speech.py
from gtts import gTTS
import os
from googletrans import Translator

def english_to_hindi(text):
    try:
        translator = Translator()
        translated = translator.translate(text, src='en', dest='hi')
        return translated.text
    except Exception as e:
        print(f"Error translating text: {e}")
        return ""

def text_to_speech(text, file_name='output.mp3', lang='hi'):
    """
    Converts the given text into speech and saves it as an MP3 file.
    :param text: The text to convert into speech.
    :param file_name: Output file name (default 'output.mp3')
    :param lang: Language code for TTS (default 'hi' for Hindi)
    :return: The absolute path to the saved audio file.
    """
    # Translate English to Hindi (if needed)
    translated_text = english_to_hindi(text)
    # Generate TTS
    tts = gTTS(text=translated_text, lang=lang, slow=False)
    tts.save(file_name)
    return os.path.abspath(file_name)
