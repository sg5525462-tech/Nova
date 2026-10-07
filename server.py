# Nova cloud server. Run: pip install fastapi uvicorn anthropic
# export ANTHROPIC_API_KEY=your_key   (key sirf server par rakho, app mein kabhi nahi)
# uvicorn server:app --host 0.0.0.0 --port 8000
import json, os
from fastapi import FastAPI
from pydantic import BaseModel
import anthropic

app = FastAPI()
client = anthropic.Anthropic()  # env var se key leta hai

SYSTEM = """You are NOVA, a voice assistant. User speaks Hindi/Hinglish/English.
Reply ONLY with JSON: {"action": "open_app" | "chat", "target": "<app name or empty>", "reply": "<short spoken reply in the user's language>"}
Use open_app only if the user asks to open an app. Otherwise action is chat."""

class Cmd(BaseModel):
    text: str

@app.post("/command")
def command(cmd: Cmd):
    try:
        msg = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=300, system=SYSTEM,
            messages=[{"role": "user", "content": cmd.text}],
        )
        raw = msg.content[0].text.strip().strip("`").removeprefix("json").strip()
        return json.loads(raw)
    except Exception:
        return {"action": "chat", "target": "", "reply": "Sorry, abhi samajh nahi paya. Dobara bolo."}
