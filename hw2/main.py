import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel

app = FastAPI(title="Embedding Service")

model = None
tokenizer = None
device = "cpu"


class TextRequest(BaseModel):
    text: str


@app.on_event("startup")
def load_model():
    global model, tokenizer
    model_name = "sergeyzh/rubert-mini-frida"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    model.eval()


@app.get("/health")
def health():
    if model is not None:
        return {"status": "ok", "model": "loaded"}
    return {"status": "error", "message": "model not initialized"}, 503


@app.post("/embed")
async def get_embedding(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Empty text")

    try:
        inputs = tokenizer(request.text, return_tensors="pt", padding=True, max_length=512).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()

        return {"embedding": embeddings[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))