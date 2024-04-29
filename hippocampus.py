from llama_cpp import Llama

def generate_topic(prompt, response):
    llm = Llama(model_path="./loyal-macaroni-maid-7b.Q6_K.gguf", n_ctx=512, n_threads=8, n_gpu_layers=32)

    system_prompt = f"Based on the following interaction between a user and an AI assistant, generate a concise topic for the conversation in 2-6 words:\n\nUser: {prompt}\nAssistant: {response}\n\nTopic:"

    topic = llm(
        system_prompt,
        max_tokens=10,
        temperature=0.7,
        stop=["\\n"],
        echo=False
    )

    return topic['choices'][0]['text'].strip()