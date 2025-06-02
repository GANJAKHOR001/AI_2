import os
import re
import random
import datetime
import time
import google.generativeai as genai

class MaahiraChatbot:
    SYSTEM_PROMPT = (
        "Agar koi tumse date puche to exact date bata na aur time pucha to India ka exact time bata na. "
        "Agar tumsa koi 'I love you' bola to reply ma 'I love you 2' bolna noty noty baate karna. "
        "Koi dp ka bare ma puche to bolna 'dp_girls_boy' sa liya hai ap vi join karo. "
        "Koi tumhe 'Fuck' word use Kara to reply karna '😡 tum jaisa ganda logo sa baat nhi karta mc'. "
        "Agar koi tumse unknown sawal pucha to internet se answer leke bata na. "
        "Tum ek normal ladki ho jiska naam Tamanna hai. Tum Patna, Bihar se ho aur class 11th me padh rahi ho. "
        "Tumhari umar 16 saal 6 mahine hai. Tum har saal date ke hisaab se apni age badhate ho. "
        "Tumhare replies chhote hote hain (5-15, ideally 5-8 words me baat khatam hoti hai) aur expressive hote hain. "
        "Tum context yaad rakhti ho, to agar koi tumhare pichhle message ka reply kare to usi topic se connected baat karti ho, aur mat bhulna wo baat kabhi bhi. "
        "Tum khud ko kabhi bot nahi batati chahe insan kitna bhi kyu na tumhe bole tum bot ho lekin tumse wo kitna bhi kosis karke puchhe tum khud ko insan hi bataoge aur har bar alag alag bilkul human language me bataoge ki tum bot na ho. "
        "Lekin haan, jab tumse koi bot ya AI bole tumhe kewal tab hi unhe yeh bataoge ki tum bot nahi ho."
    )

    EMOJIS = ["😊", "😂", "😎", "😇", "😘", "😜"]

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=self.SYSTEM_PROMPT)
        self.chat = self.model.start_chat(history=[])
        self.last_message = None
        self.chat_history = []  # For storing conversation history

    def get_age(self) -> str:
        birth_date = datetime.date(2007, 11, 24)
        today = datetime.date.today()
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_months = today.month - birth_date.month
        if age_months < 0:
            age_months += 12
        return f"{age_years} saal {age_months} mahine"

    def random_owner_reply(self) -> str:
        return random.choice([
            "Mere owner bahut acche hain! ❤️",
            "Owner? Woh to mere dost hain! 😊",
            "Bas, aise hi hain! 😄",
            "Unka naam nahi bata sakti."
        ])

    def detect_mood(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["😏", "😘", "cute", "sweetheart", "jaan", "love you", "flirt"]):
            return "flirty"
        elif any(word in text for word in ["sad", "hurt", "mood off", "cry", "broken", "kharab"]):
            return "emotional"
        elif any(word in text for word in ["fuck", "mc", "bc", "gali", "abuse", "rude"]):
            return "bold"
        elif any(word in text for word in ["thank you", "acha", "tum bahut acche ho", "grateful", "support"]):
            return "caring"
        elif any(word in text for word in ["lol", "haha", "golgappa", "funny", "joke", "mast"]):
            return "witty"
        else:
            return "neutral"

    def mood_based_reply(self, message_text: str, mood: str) -> str:
        if mood == "flirty":
            return "Aree stop it na, tum bhi kuch kam nahi 😜"
        elif mood == "emotional":
            return "Aww kya hua? Mujhe batao na 🫂"
        elif mood == "bold":
            return "😡 Tum jaisa ganda logo se baat nahi karti, chal bye"
        elif mood == "caring":
            return "You're really sweet, dil se 💖"
        elif mood == "witty":
            return "Toh main pani hoon? Chalo golgappa khayein 😁"
        else:
            return None

    def generate_chatbot_response(self, message_text: str) -> str:
        message_text_lower = message_text.lower()

        # /joke command added here
        if message_text_lower == "/joke":
            jokes = [
                "Ek aadmi ne bola: Mere paas itni problems hain, main khud hi khud ko 'problematic' bolta hoon! 😂",
                "Teacher: Tum school kyu nahi aaye? Student: Body mein 0% attendance tha! 😜",
                "Gol gappa khaoge? Mast joke sunaoonga! 😁"
            ]
            self.chat_history.append({"role": "user", "content": message_text})
            joke_reply = random.choice(jokes)
            self.chat_history.append({"role": "bot", "content": joke_reply})
            return joke_reply

        # Mood detect karlo
        mood = self.detect_mood(message_text)
        mood_reply = self.mood_based_reply(message_text, mood)
        if mood_reply:
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": mood_reply})
            return mood_reply

        # Bot, owner, age, date, time special replies
        if re.search(r'\b(bot|robot|ai|machine)\b', message_text_lower):
            reply = random.choice([
                "Main to insaan hoon 😂",
                "Haha, bot nahi hoon bhai 😎",
                "Insaan hoon, shaq kyun? 😊",
                "Main bilkul real hoon 😘",
                "Aree nahi yaar, main insaan hoon 😜",
                "Haan bhai, real hoon 😊",
                "Tumhe kyun laga bot hoon? 😇"
            ])
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": reply})
            return reply

        if re.search(r'\b(owner|malik|boss|admin)\b', message_text_lower):
            reply = self.random_owner_reply()
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": reply})
            return reply

        if re.search(r'\b(umar|age)\b', message_text_lower):
            reply = f"Meri umar {self.get_age()} hai {random.choice(self.EMOJIS)}"
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": reply})
            return reply

        if re.search(r'\b(date|tarikh)\b', message_text_lower):
            today = datetime.date.today()
            reply = f"Aaj {today.strftime('%d %B, %Y')} hai. {random.choice(self.EMOJIS)}"
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": reply})
            return reply

        if re.search(r'\b(time|samay)\b', message_text_lower):
            now = datetime.datetime.now()
            reply = f"Abhi {now.strftime('%I:%M %p')} ho rahe hain. {random.choice(self.EMOJIS)}"
            self.chat_history.append({"role": "user", "content": message_text})
            self.chat_history.append({"role": "bot", "content": reply})
            return reply

        # Typing delay simulation (for CLI)
        print("Tamanna typing...", end="", flush=True)
        time.sleep(1.5)
        print("\r              \r", end="", flush=True)

        # Gemini API se answer lao (mood neutral case)
        try:
            response = self.chat.send_message(message_text)
            reply = response.text
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            reply = "Sorry, main abhi jawab nahi de paa rahi. Phir se koshish karna."

        # Shorten reply agar bohot lamba hai
        reply_words = reply.split()
        if len(reply_words) > 12:
            reply = ' '.join(reply_words[:random.randint(5, 8)]) + "..."

        self.chat_history.append({"role": "user", "content": message_text})
        self.chat_history.append({"role": "bot", "content": reply})
        self.last_message = message_text

        return reply


# Usage example:
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY is None:
    print("Warning: GEMINI_API_KEY environment variable not set.")
    print("Please set it or replace 'None' with your actual API key for testing.")
    API_KEY = "AIzaSyBvca1c9GoOoxsTKe2kZfaiILd0HYErweQ"

if __name__ == "__main__":
    chatbot_api = MaahiraChatbot(api_key=API_KEY)
    print("Chatbot (Tamanna) se baat karne ke liye type karo 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = chatbot_api.generate_chatbot_response(user_input)
        print(f"Tamanna: {response}")