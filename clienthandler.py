from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pmbl import PMBL

app = FastAPI()
pmbl = PMBL("./loyal-macaroni-maid-7b.Q6_K.gguf")  # Replace with the path to your model

templates = Jinja2Templates(directory="templates")

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data["user_input"]
        mode = data["mode"]
        history = pmbl.get_chat_history(mode, user_input)
        response_generator = pmbl.generate_response(user_input, history, mode)
        return StreamingResponse(response_generator, media_type="text/plain")
    except Exception as e:
        print(f"[SYSTEM] Error: {str(e)}")
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/sleep")
async def sleep():
    try:
        pmbl.sleep_mode()
        return {"message": "Sleep mode completed successfully"}
    except Exception as e:
        print(f"[SYSTEM] Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1771)