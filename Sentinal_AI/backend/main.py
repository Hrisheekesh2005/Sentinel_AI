from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import analyze_message

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Sentinel API is running 🚀"}


class Message(BaseModel):
    message: str


@app.post("/analyze")
def analyze(msg: Message):
    return analyze_message(msg.message)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import analyze_message
import uvicorn

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Sentinel API is running successfully 🚀"}

class Message(BaseModel):
    message: str

@app.post("/analyze")
def analyze(msg: Message):
    # Calls the integrated analyze_message from agent.py
    return analyze_message(msg.message)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)