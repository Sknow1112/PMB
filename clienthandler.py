from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pmbl import PMBL

app = FastAPI()
pmbl = PMBL("")

templates = Jinja2Templates(directory="templates")

@app.post("/chat")
async def chat(request: Request):
    user_input = (await request.json())["user_input"]
    history = pmbl.get_chat_history()
    response = pmbl.generate_response(user_input, history)
    return {"response": response}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)