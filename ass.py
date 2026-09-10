import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import json
import requests
from typing import Optional

class AIAssistant:
    def __init__(self, name: str = "Assistant"):
        self.name = name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
        
        # Load user preferences
        self.preferences = self.load_preferences()
        
    def setup_voice(self):
        """Configure TTS voice settings"""
        voices = self.tts_engine.getProperty('voices')
        # Set voice (0 for male, 1 for female typically)
        self.tts_engine.setProperty('voice', voices[1].id)
        # Set speech rate
        self.tts_engine.setProperty('rate', 180)
        # Set volume
        self.tts_engine.setProperty('volume', 0.9)
    
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self) -> Optional[str]:
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech service.")
            return None
    
    def load_preferences(self) -> dict:
        """Load user preferences from file"""
        try:
            with open('preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "name": "User",
                "city": "London",
                "units": "metric"
            }
    
    def save_preferences(self):
        """Save user preferences to file"""
        with open('preferences.json', 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def get_time(self) -> str:
        """Get current time"""
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")
    
    def get_date(self) -> str:
        """Get current date"""
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y")
    
    def get_weather(self, city: str = None) -> str:
        """Get weather information (requires API key)"""
        city = city or self.preferences.get("city", "London")
        # Using OpenWeatherMap API (you'll need to sign up for a free API key)
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"The weather in {city} is {desc} with a temperature of {temp:.1f}°C"
            else:
                return f"Sorry, I couldn't get the weather for {city}"
        except Exception as e:
            return "Sorry, I couldn't fetch the weather information"
    
    def search_web(self, query: str):
        """Search the web"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching for {query}"
    
    def open_application(self, app_name: str) -> str:
        """Open applications (platform-specific)"""
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": "chrome.exe",
            "terminal": "cmd.exe" if os.name == 'nt' else "gnome-terminal",
        }
        
        app_name = app_name.lower()
        if app_name in apps:
            try:
                os.system(f"start {apps[app_name]}" if os.name == 'nt' else f"{apps[app_name]} &")
                return f"Opening {app_name}"
            except Exception:
                return f"Couldn't open {app_name}"
        return f"I don't know how to open {app_name}"
    
    def tell_joke(self) -> str:
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ]
        return random.choice(jokes)
    
    def calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Only allow safe mathematical operations
            allowed_chars = set("0123456789+-*/(). ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"The result is {result}"
            else:
                return "Sorry, I can only do basic math"
        except:
            return "Sorry, I couldn't calculate that"
    
    def process_command(self, command: str) -> bool:
        """Process user command and return False to exit"""
        
        # Greetings
        if any(word in command for word in ["hello", "hi", "hey"]):
            self.speak(f"Hello {self.preferences['name']}! How can I help you?")
        
        # Time
        elif "time" in command:
            self.speak(f"The current time is {self.get_time()}")
        
        # Date
        elif "date" in command or "day" in command:
            self.speak(f"Today is {self.get_date()}")
        
        # Weather
        elif "weather" in command:
            # Extract city name if mentioned
            words = command.split()
            city = None
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = words[idx + 1]
            self.speak(self.get_weather(city))
        
        # Search
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            if query:
                self.speak(self.search_web(query))
            else:
                self.speak("What would you like me to search for?")
        
        # Open applications
        elif "open" in command:
            app = command.replace("open", "").strip()
            self.speak(self.open_application(app))
        
        # Jokes
        elif "joke" in command:
            self.speak(self.tell_joke())
        
        # Math
        elif any(word in command for word in ["calculate", "compute", "what is"]):
            expression = command.replace("calculate", "").replace("compute", "").replace("what is", "").strip()
            self.speak(self.calculate(expression))
        
        # Name
        elif "your name" in command:
            self.speak(f"My name is {self.name}")
        
        # Change name
        elif "call me" in command:
            name = command.replace("call me", "").strip()
            self.preferences["name"] = name
            self.save_preferences()
            self.speak(f"I'll call you {name} from now on")
        
        # Exit commands
        elif any(word in command for word in ["exit", "quit", "bye", "goodbye"]):
            self.speak(f"Goodbye {self.preferences['name']}! Have a great day!")
            return False
        
        # Help
        elif "help" in command:
            help_text = """Here are some things I can do:
            - Tell you the time and date
            - Check the weather
            - Search the web
            - Open applications
            - Tell jokes
            - Do calculations
            - And more!"""
            self.speak(help_text)
        
        else:
            self.speak("I'm not sure how to help with that. Say 'help' for available commands.")
        
        return True
    
    def run_voice_mode(self):
        """Run the assistant in voice mode"""
        self.speak(f"Hello! I'm {self.name}, your AI assistant. How can I help you?")
        
        while True:
            command = self.listen()
            if command:
                if not self.process_command(command):
                    break
    
    def run_text_mode(self):
        """Run the assistant in text mode"""
        self.speak(f"Hello! I'm {self.name}, your AI assistant. Type 'help' for commands or 'exit' to quit.")
        
        while True:
            try:
                command = input("\nYou: ").lower().strip()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                self.speak("\nGoodbye!")
                break
    
    def run(self, mode: str = "text"):
        """Run the assistant in specified mode"""
        if mode == "voice":
            self.run_voice_mode()
        else:
            self.run_text_mode()


# Simple rule-based chatbot (alternative lightweight version)
class SimpleAIAssistant:
    def __init__(self, name="Assistant"):
        self.name = name
        self.responses = {
            "greeting": ["Hello!", "Hi there!", "Hey! How can I help?"],
            "farewell": ["Goodbye!", "See you later!", "Take care!"],
            "thanks": ["You're welcome!", "Happy to help!", "Anytime!"],
            "default": ["I'm not sure about that.", "Could you rephrase?", "Interesting!"]
        }
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return random.choice(self.responses["greeting"])
        elif any(word in user_input for word in ["bye", "goodbye", "exit"]):
            return random.choice(self.responses["farewell"])
        elif "thank" in user_input:
            return random.choice(self.responses["thanks"])
        elif "time" in user_input:
            return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
        elif "date" in user_input:
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        else:
            return random.choice(self.responses["default"])


if __name__ == "__main__":
    # Choose which assistant to use
    print("Select assistant mode:")
    print("1. Full AI Assistant (text mode)")
    print("2. Full AI Assistant (voice mode)")
    print("3. Simple AI Assistant")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        assistant = AIAssistant("Jarvis")
        assistant.run("text")
    elif choice == "2":
        assistant = AIAssistant("Jarvis")
        assistant.run("voice")
    elif choice == "3":
        assistant = SimpleAIAssistant("ChatBot")
        print(f"{assistant.name}: Hello! Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if "exit" in user_input.lower() or "bye" in user_input.lower():
                print(f"{assistant.name}: {assistant.get_response(user_input)}")
                break
            print(f"{assistant.name}: {assistant.get_response(user_input)}")
    else:
        print("Invalid choice")