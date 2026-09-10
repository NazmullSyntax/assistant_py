# Save as: assistant.py
import datetime
import random
import webbrowser
import os

class SimpleAssistant:
    def __init__(self, name="Jarvis"):
        self.name = name
        self.user_name = "User"
    
    def speak(self, text):
        """Print only - no TTS needed"""
        print(f"{self.name}: {text}")
    
    def get_time(self):
        return datetime.datetime.now().strftime("%I:%M %p")
    
    def get_date(self):
        return datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
        ]
        return random.choice(jokes)
    
    def calculate(self, expr):
        try:
            allowed = set("0123456789+-*/(). ")
            if all(c in allowed for c in expr):
                return f"Result: {eval(expr)}"
            return "Only basic math allowed."
        except:
            return "Couldn't calculate that."
    
    def process(self, command):
        cmd = command.lower().strip()
        
        if any(w in cmd for w in ["hello", "hi", "hey"]):
            self.speak(f"Hello {self.user_name}! How can I help?")
        elif "time" in cmd:
            self.speak(f"The time is {self.get_time()}")
        elif "date" in cmd or "day" in cmd:
            self.speak(f"Today is {self.get_date()}")
        elif "joke" in cmd:
            self.speak(self.tell_joke())
        elif "search" in cmd:
            query = cmd.replace("search", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                self.speak(f"Searching for {query}")
            else:
                self.speak("What should I search for?")
        elif "open notepad" in cmd:
            os.system("start notepad.exe")
            self.speak("Opening Notepad")
        elif "open calculator" in cmd or "open calc" in cmd:
            os.system("start calc.exe")
            self.speak("Opening Calculator")
        elif any(w in cmd for w in ["calculate", "compute"]):
            expr = cmd.replace("calculate", "").replace("compute", "").strip()
            self.speak(self.calculate(expr))
        elif "your name" in cmd:
            self.speak(f"My name is {self.name}")
        elif "call me" in cmd:
            self.user_name = cmd.replace("call me", "").strip().title()
            self.speak(f"Nice to meet you, {self.user_name}!")
        elif "help" in cmd:
            self.speak("Commands: hello, time, date, joke, search <query>, open notepad, calculate <expr>, call me <name>, exit")
        elif any(w in cmd for w in ["exit", "quit", "bye"]):
            self.speak(f"Goodbye {self.user_name}!")
            return False
        else:
            self.speak("I don't understand. Type 'help' for commands.")
        return True
    
    def run(self):
        self.speak(f"Hello! I'm {self.name}. Type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                cmd = input("\nYou: ").strip()
                if cmd and not self.process(cmd):
                    break
            except KeyboardInterrupt:
                self.speak("\nGoodbye!")
                break


if __name__ == "__main__":
    SimpleAssistant("Jarvis").run()