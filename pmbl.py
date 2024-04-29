import sqlite3
from datetime import datetime
from llama_cpp import Llama
from hippocampus import generate_topic

class PMBL:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path, n_ctx=4096, n_threads=8, n_gpu_layers=32)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chats
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT,
                     prompt TEXT,
                     response TEXT,
                     topic TEXT)''')
        conn.commit()
        conn.close()

    def get_chat_history(self, mode="full", user_message=""):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()

        if mode == "full":
            c.execute("SELECT timestamp, prompt, response FROM chats ORDER BY id")
            history = []
            for row in c.fetchall():
                history.append({"role": "user", "content": row[1]})
                history.append({"role": "PMB", "content": f"[{row[0]}] {row[2]}"})
        else:  # mode == "smart"
            c.execute("SELECT id, prompt, response FROM chats WHERE topic != 'Untitled'")
            chats = c.fetchall()
            relevant_chat_id = self.find_relevant_chat(chats, user_message)

            if relevant_chat_id:
                c.execute("SELECT timestamp, prompt, response FROM chats WHERE id = ?", (relevant_chat_id,))
                row = c.fetchone()
                history = [
                    {"role": "user", "content": row[1]},
                    {"role": "PMB", "content": f"[{row[0]}] {row[2]}"}
                ]
            else:
                history = []

        conn.close()
        return history

    def find_relevant_chat(self, chats, user_message):
        max_score = 0
        relevant_chat_id = None

        for chat in chats:
            chat_id, prompt, response = chat
            score = self.calculate_similarity_score(prompt + " " + response, user_message)

            if score > max_score:
                max_score = score
                relevant_chat_id = chat_id

        return relevant_chat_id

    def calculate_similarity_score(self, text1, text2):
        words1 = text1.lower().split()
        words2 = text2.lower().split()

        score = 0
        for i in range(len(words1) - 1):
            if words1[i] in words2 and words1[i + 1] in words2:
                score += 1

        return score

    def save_chat_history(self, prompt, response):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO chats (timestamp, prompt, response, topic) VALUES (?, ?, ?, 'Untitled')", (timestamp, prompt, response))
        conn.commit()
        conn.close()

    def generate_response(self, prompt, history, mode):
        history.append({"role": "user", "content": prompt})

        formatted_history = ""
        for message in history:
            formatted_history += f"{message['role']}: {message['content']}\n"

        if mode == "full":
            system_prompt = f"You are an intelligent assistant named PMB - Persistent Memory Bot. Previous conversations between you and the user are below for your reference. Don't mention a topic unless the user brings it up again. Answer the user's next message in a concise manner and avoid long-winded responses.\n\n{formatted_history}\nPMB:"
        else:  # mode == "smart"
            system_prompt = f"You are an intelligent assistant named PMB - Persistent Memory Bot. The user has asked a question related to a previous conversation. The relevant conversation is provided below for context. Answer the user's question based on the context and your knowledge. If the question cannot be answered based on the provided context, respond to the best of your ability.\n\n{formatted_history}\nPMB:"

        response = self.llm(
            system_prompt,
            max_tokens=1500,
            temperature=0.7,
            stop=["</s>", "\nUser:", "\nuser:", "\nSystem:", "\nsystem:"],
            echo=False,
            stream=True
        )

        response_text = ""
        for chunk in response:
            chunk_text = chunk['choices'][0]['text']
            response_text += chunk_text
            yield chunk_text

        self.save_chat_history(prompt, response_text)

    def sleep_mode(self):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute("SELECT id, prompt, response FROM chats WHERE topic = 'Untitled'")
        untitled_chats = c.fetchall()

        for chat in untitled_chats:
            chat_id, prompt, response = chat
            topic = generate_topic(prompt, response)
            c.execute("UPDATE chats SET topic = ? WHERE id = ?", (topic, chat_id))
            conn.commit()

        conn.close()