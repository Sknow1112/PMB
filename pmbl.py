import sqlite3
from datetime import datetime
from llama_cpp import Llama


class PMBL:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path, n_ctx=29000, n_threads=8, n_gpu_layers=35)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chats
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT,
                     prompt TEXT,
                     response TEXT)''')
        conn.commit()
        conn.close()

    def get_chat_history(self):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute("SELECT timestamp, prompt, response FROM chats")
        history = [{"role": "system",
                    "content": "You are an intelligent assistant named PMB - Persistent Memory Bot. You always provide well-reasoned answers that are consise, correct and helpful"}]
        for row in c.fetchall():
            history.append({"role": "assistant", "content": f"[{row[0]}] {row[2]}"})
            history.append({"role": "user", "content": row[1]})
        conn.close()
        return history

    def save_chat_history(self, prompt, response):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO chats (timestamp, prompt, response) VALUES (?, ?, ?)", (timestamp, prompt, response))
        conn.commit()
        conn.close()

    def generate_response(self, prompt, history):
        history.append({"role": "user", "content": prompt})

        messages = [
            {"role": "system",
             "content": "You are an intelligent assistant named PMB - Persistent Memory Bot. You always provide well-reasoned answers that are often short, consise, correct and helpful."}
        ]
        messages.extend(history)

        formatted_messages = ""
        for message in messages:
            formatted_messages += f"{message['role']}: {message['content']}\n"

        prompt_with_history = f"Below is the conversation history for your reference. Don't mention a topic unless the user brings it up.\n\n{formatted_messages}\nAssistant:"

        response = self.llm(
            prompt_with_history,
            max_tokens=29000,
            temperature=0.7,
            stop=["</s>", "\nHuman:"],
            echo=False
        )

        response_text = response['choices'][0]['text'].strip()

        self.save_chat_history(prompt, response_text)

        return response_text