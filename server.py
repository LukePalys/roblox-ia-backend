from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Prompt(BaseModel):
    text: str

@app.post("/generate")
def generate_script(data: Prompt):
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=f"Você é especialista em Roblox Studio. Crie um script Luau para: {data.text}",
        max_tokens=800,
        temperature=0
    )
    return {"result": response.choices[0].text.strip()}

@app.post("/review")
async def review_script(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=f"Revise e explique este script do Roblox Studio:\ncode",
        max_tokens=800,
        temperature=0
    )
    return {"result": response.choices[0].text.strip()}

@app.get("/")
def root():
    return {"status": "API Roblox IA funcionando!"}

if _name_ == "_main_":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

