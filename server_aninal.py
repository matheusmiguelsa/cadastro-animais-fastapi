from fastapi import FastAPI
import uvicorn
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Animal(BaseModel):
    id: Optional[int]
    nome: str
    idade: int
    sexo: str
    cor: str


banco: List[Animal] = []


@app.get("/")
async def home():
    return {"message": "Hello World!"}


@app.get("/animais")
async def listar_animais():
    return banco


@app.get("/animais/{id}")
async def listar_animal(id):
    for animal in banco:
        if animal.id == id:
            return animal


@app.delete("/animais/{id}")
async def deletar_animal(id):
    for animal in banco:
        if animal.id == id:
            banco.remove(animal)
            return "animal deletado"


@app.post("/animais")
async def criar_animal(novo_animal: Animal):
    novo_animal.id = str(uuid4())
    banco.append(novo_animal)
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
