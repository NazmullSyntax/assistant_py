import datetime
import os
import re
import webbrowser

try:
    from google import genai as google_genai
except Exception:
    google_genai = None

try:
    import google.generativeai as legacy_genai
except Exception:
    legacy_genai = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# ====== CONFIG ======
API_KEY = "PASTE_YOUR_API_KEY_HERE"
MODEL_NAME = "gemini-1.5-flash"
# ====================

GOOGLE_SDK_AVAILABLE = google_genai is not None or legacy_genai is not None

if GOOGLE_SDK_AVAILABLE and API_KEY and API_KEY != "PASTE_YOUR_API_KEY_HERE":
    if google_genai is not None:
        try:
            google_client = google_genai.Client(api_key=API_KEY)
        except Exception:
            google_client = None
    else:
        google_client = None

    if google_client is None and legacy_genai is not None:
        try:
            legacy_genai.configure(api_key=API_KEY)
            model = legacy_genai.GenerativeModel(MODEL_NAME)
        except Exception:
            model = None
    else:
        model = None
else:
    google_client = None
    model = None

if pyttsx3 is not None:
    try:
        tts = pyttsx3.init()
        tts.setProperty("rate", 180)
        VOICE_ENABLED = True
    except Exception:
        tts = None
        VOICE_ENABLED = False
else:
    tts = None
    VOICE_ENABLED = False


class GeminiAssistant:
    def __init__(self, name="Nova"):
        self.name = name
        self.chat = None
        self.system_context = (
            f"You are {name}, a helpful, friendly AI assistant running on the user's "
            f"Windows PC. Keep answers concise (1-3 sentences) unless asked for detail. "
            f"Current date/time: {datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}. "
            f"If the user asks to open an app, search the web, or run something, "
            f"reply in the format: ACTION:<action>|<value> at the END of your message."
        )

        if google_client is not None:
            self.chat = google_client
        elif model is not None:
            self.chat = model.start_chat(history=[])

    def speak(self, text):
        print(f"{self.name}: {text}")
        if VOICE_ENABLED and tts is not None:
            try:
                tts.say(text)
                tts.runAndWait()
            except Exception:
                pass

    def handle_actions(self, reply):
        """Detect ACTION:...|... tags and run local commands."""
        actions = re.findall(r"ACTION:(\w+)\|([^\n]+)", reply)
        for action, value in actions:
            value = value.strip()
            if action == "open_app":
                apps = {
                    "notepad": "notepad.exe",
                    "calculator": "calc.exe",
                    "calc": "calc.exe",
                    "paint": "mspaint.exe",
                    "cmd": "cmd.exe",
                    "explorer": "explorer.exe",
                }
                exe = apps.get(value.lower())
                if exe:
                    os.system(f"start {exe}")
                    print(f"  [Opened {value}]")
            elif action == "search":
                webbrowser.open(
                    f"https://www.google.com/search?q={value.replace(' ', '+')}"
                )
                print(f"  [Searching: {value}]")
            elif action == "youtube":
                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={value.replace(' ', '+')}"
                )
                print(f"  [YouTube: {value}]")

        clean = re.sub(r"ACTION:\w+\|[^\n]+", "", reply).strip()
        return clean

    def _offline_fallback(self, user_input):
        text = user_input.lower().strip()

        if any(word in text for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help?"
        if "time" in text:
            return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
        if "date" in text or "day" in text:
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        if "search" in text:
            query = text.replace("search", "").strip()
            if query:
                return f"Searching for {query}. ACTION:search|{query}"
            return "What would you like me to search for?"
        if "notepad" in text:
            return "Opening Notepad. ACTION:open_app|notepad"
        if "calculator" in text or "calc" in text:
            return "Opening Calculator. ACTION:open_app|calculator"
        if "youtube" in text:
            query = text.replace("youtube", "").strip() or "popular videos"
            return f"Opening YouTube results for {query}. ACTION:youtube|{query}"
        if "your name" in text:
            return f"My name is {self.name}."
        if "bye" in text or "goodbye" in text or "exit" in text:
            return "Goodbye!"
        return (
            "Gemini is not configured in this environment yet. "
            "Add your API key in the script or install the required Google SDK to enable live AI responses."
        )

    def ask(self, user_input):
        if self.chat is None:
            reply = self._offline_fallback(user_input)
            clean = self.handle_actions(reply)
            if clean:
                self.speak(clean)
            return

        try:
            if hasattr(self.chat, "models"):
                response = self.chat.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"{self.system_context}\n\nUser: {user_input}",
                )
                raw = getattr(response, "text", str(response))
            else:
                response = self.chat.send_message(
                    f"{self.system_context}\n\nUser: {user_input}"
                )
                raw = response.text

            clean = self.handle_actions(raw)
            if clean:
                self.speak(clean)
        except Exception as e:
            self.speak(f"Sorry, I hit an error: {e}")

    def run(self):
        self.speak(f"Hi! I'm {self.name}. Ask me anything. Type 'exit' to quit.")
        while True:
            try:
                user = input("\nYou: ").strip()
                if not user:
                    continue
                if user.lower() in ["exit", "quit", "bye"]:
                    self.speak("Goodbye!")
                    break
                self.ask(user)
            except KeyboardInterrupt:
                self.speak("\nBye!")
                break


if __name__ == "__main__":
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("⚠️  No Gemini API key found. The assistant will run in offline fallback mode.")
    elif not GOOGLE_SDK_AVAILABLE:
        print("⚠️  Google AI SDK is not installed. The assistant will run in offline fallback mode.")
    GeminiAssistant("Nova").run()