import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import wave
from vosk import Model, KaldiRecognizer

AudioSegment.ffmpeg = "/usr/bin/ffmpeg /usr/share/ffmpeg /usr/share/man/man1/ffmpeg.1.gz"
translator = Translator()
recognizer = sr.Recognizer()

languages = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yiddish': 'yi'
}

emoji_dict = {
    "happy": "😊",
    "love": "❤️",
    "sad": "😢",
    "angry": "😠",
    "sun": "☀️",
    "star": "⭐",
    "heart": "❤️",
    "laugh": "😂",
    "cry": "😭",
    "car": "🚗",
    "phone": "📱",
    "fire": "🔥",
    "cool": "😎",
    "food": "🍲",
    "dog": "🐕",
    "cat": "🐈",
}


def replace_with_emojis(text):
    words = text.split()
    new_text = []
    for word in words:
        new_text.append(emoji_dict.get(word.lower(), word))
    return " ".join(new_text)


def speech_to_text_vosk(model_path, audio_file):
    model = Model(model_path)
    wf = wave.open(audio_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            results.append(result)

    return ' '.join(results)


def text_to_speech(text, lang_code):
    tts = gTTS(text, lang=lang_code)
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file


def audio_player(audio_file):
    try:
        audio_file.seek(0)
        audio = AudioSegment.from_file(audio_file, format="wav")  
        st.audio(audio_file, format="audio/wav")
    except CouldntDecodeError:
        st.error("Error decoding the audio file. Ensure the file is in a supported format and not corrupted.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
st.title("Global Translator Chatbot with Emojis and Speech Features")

input_method = st.radio("Choose Input Method:", ['Text', 'Speech'])

vosk_model_path = 'path_to_your_vosk_model'

if input_method == 'Speech':
    audio_file = st.file_uploader("Upload audio file (WAV format):", type='wav')

    if audio_file:
        st.write(f"Uploaded file: {audio_file.name}")
        st.write(f"File size: {audio_file.size} bytes")

else:
    text = st.text_area("Enter text to translate:")

target_language = st.selectbox("Choose the target language:", list(languages.keys()))
target_lang_code = languages[target_language]

if st.button("Translate"):
    if text:
        translated_text = translator.translate(text, dest=target_lang_code).text
        st.success(f"Translated text: {translated_text}")

        translated_with_emojis = replace_with_emojis(translated_text)
        st.success(f"Translated text with emojis: {translated_with_emojis}")

        st.subheader("Text-to-Speech (TTS) Output:")
        audio_file = text_to_speech(translated_with_emojis, target_lang_code)
        audio_player(audio_file)
    else:
        st.error("Please enter or speak text to translate.")
