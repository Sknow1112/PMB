from fastapi import FastAPI, Request
from pydantic import BaseModel
from pmbl import PMBL

app = FastAPI()
pmbl = PMBL("./silicon-maid-7b.Q4_K_M.gguf")

class UserInput(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(user_input: UserInput):
    history = pmbl.get_chat_history()
    response = pmbl.generate_response(user_input.prompt, history)
    return {"response": response}

@app.get("/")
async def root():
    return {"message": "Welcome to the Persistent Memory Bot (PMB)!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)