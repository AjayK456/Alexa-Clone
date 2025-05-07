import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# List available voices (Debugging)
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name}")

# Set the voice (Try different indexes if needed)
engine.setProperty('voice', voices[1].id)

# Function to make Alexa speak
def talk(text):
    print(f"Alexa says: {text}")  # Debugging output
    engine.say(text)
    engine.runAndWait()  # ✅ Ensure this is called every time

# Function to take voice command
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)  # Reduce background noise
            voice = listener.listen(source)  # Capture voice input
            command = listener.recognize_google(voice)  # Convert speech to text
            command = command.lower()

            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(f"Command received: {command}")  # Debugging output
                return command
    except sr.UnknownValueError:
        talk("Sorry, I could not understand you.")
    except sr.RequestError:
        talk("I cannot access the internet right now.")
    except Exception as e:
        print(f"An error occurred: {e}")
        talk("An error occurred.")

    return ""

# Function to process commands
def run_alexa():
    command = take_command()

    if command:
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"Current time is {time}")
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            try:
                info = wikipedia.summary(person, 1)
                talk(info)
            except wikipedia.exceptions.PageError:
                talk(f"Sorry, I couldn't find information about {person}")
        elif 'date' in command:
            talk("Sorry, I have a headache.")
        elif 'are you single' in command:
            talk("I am in a relationship with WiFi.")
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)
        else:
            talk("Please say the command again.")

# Keep running Alexa in a loop
while True:
    run_alexa()
