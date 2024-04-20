import json
import sqlite3
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from datetime import datetime

app = Flask(__name__)
client = OpenAI(base_url="http://localhost:1771/v1", api_key="lm-studio")

# Initialize the database
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT,
                 prompt TEXT,
                 response TEXT)''')
    conn.commit()
    conn.close()

# Retrieve chat history from the database
def get_chat_history():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, prompt, response FROM chats")
    history = [{"role": "system", "content": "You are an intelligent assistant named PMB - Persistent Memory Bot. You always provide well-reasoned answers that are both correct and helpful."}]
    for row in c.fetchall():
        history.append({"role": "assistant", "content": f"[{row[0]}] {row[2]}"})
        history.append({"role": "user", "content": row[1]})
    conn.close()
    return history

# Save chat history to the database
def save_chat_history(prompt, response):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO chats (timestamp, prompt, response) VALUES (?, ?, ?)", (timestamp, prompt, response))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    history = get_chat_history()
    history.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="model-identifier",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content

    save_chat_history(user_input, response)

    return jsonify(response=response)

if __name__ == '__main__':
    init_db()
    app.run()