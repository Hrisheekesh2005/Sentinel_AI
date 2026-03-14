import speech_recognition as sr
import requests

API_URL = "http://127.0.0.1:8000/analyze"

recognizer = sr.Recognizer()

print("🎤 Voice Scam Detection Started")
print("Speak a message...\n")

with sr.Microphone() as source:

    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("🎤 Listening...")

    audio = recognizer.listen(source)

    print("Processing voice...")

    try:
        text = recognizer.recognize_google(audio)

        print("\n📝 Transcribed Text:")
        print(text)

        # Send voice text to your AI scam detector
        response = requests.post(API_URL, json={"message": text})
        result = response.json()

        print("\n🤖 AI Scam Detection Result:")
        print(result)

        if result.get("decision") == "SUSPICIOUS" or result.get("decision") == "SCAM":
            print("\n⚠ WARNING: Possible Scam Voice Message")

    except sr.UnknownValueError:
        print("❌ Could not understand audio")

    except sr.RequestError:
        print("❌ Speech recognition service error")