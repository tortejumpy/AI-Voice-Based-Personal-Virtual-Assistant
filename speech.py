import google.generativeai as genai
import pyttsx3  # For text-to-speech
import speech_recognition as sr  # For speech recognition
from googletrans import Translator  # For translation

# Google Generative AI configuration
GOOGLE_API_KEY = ''
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Initialize text-to-speech engine
engine = pyttsx3.init()
translator = Translator()

# Language configurations
LANGUAGES = {
    "english": ("en", "en"),
    "spanish": ("es", "es"),
    "german": ("de", "de"),
    "french": ("fr", "fr"),
    "roman": ("ro", "ro"),
    "italian": ("it", "it")  # Added Italian support
}

def set_tts_language(language_code):
    """Set TTS engine to the appropriate language."""
    voices = engine.getProperty('voices')
    for voice in voices:
        if hasattr(voice, 'languages') and voice.languages:
            if language_code in str(voice.languages):
                engine.setProperty('voice', voice.id)
                return
    engine.setProperty('voice', voices[0].id)

def speak(text, language_code):
    """Convert text to speech in the specified language."""
    set_tts_language(language_code)
    engine.say(text)
    engine.runAndWait()

def listen(language="en"):
    """Take voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("Processing voice input...")
            text = recognizer.recognize_google(audio, language=language)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please try again.")
            speak("Sorry, I did not understand that. Please try again.", language)
        except sr.RequestError:
            print("Could not request results. Please check your internet connection.")
            speak("Could not request results. Please check your internet connection.", language)
    return None

def main():
    """Main function for multilingual interaction."""
    print("Please choose a language (English, Spanish, German, French, Roman, Italian):")
    speak("Please choose a language: English, Spanish, German, French, Roman, or Italian.", "en")
    user_choice = None

    # Keep prompting until a valid language is selected
    while user_choice is None:
        user_choice = listen("en")
        if user_choice is None:
            continue
        user_choice = user_choice.lower()

    selected_language = "english"  # Default to English
    for lang in LANGUAGES:
        if lang in user_choice:
            selected_language = lang
            break

    language_code, recognition_language = LANGUAGES[selected_language]
    print(f"Language selected: {selected_language.capitalize()}")
    speak(f"Language selected: {selected_language.capitalize()}", language_code)

    while True:
        print(f"Speak your query in {selected_language.capitalize()} (say 'exit' to quit):")
        user_input = listen(recognition_language)
        
        if user_input is None:  # If input is not recognized, prompt again
            print("I didn't catch that. Please try again.")
            speak("I didn't catch that. Please try again.", language_code)
            continue

        if "exit" in user_input.lower():
            print("Exiting... Goodbye!")
            speak("Exiting. Goodbye!", language_code)
            break

        # Translate user input to English for AI processing (if needed)
        if selected_language != "english":
            user_input = translator.translate(user_input, src=language_code, dest="en").text

        # Send query to Google Generative AI
        response = chat.send_message(user_input)
        response_text = response.text

        # Translate response back to the user's language
        if selected_language != "english":
            response_text = translator.translate(response_text, src="en", dest=language_code).text

        print(f"AI Response: {response_text}")
        speak(response_text, language_code)

if __name__ == "__main__":
    main()
