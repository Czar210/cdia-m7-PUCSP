from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

reservas = [
    {"id": 1, "mesa": 5, "nome": "Silva", "pessoas": 4, "ativa": True},
    {"id": 2, "mesa": 3, "nome": "Costa", "pessoas": 2, "ativa": False},
]

class ReservaInput(BaseModel):
    mesa: int
    nome: str
    pessoas: int

@app.get("/reservas/{reserva_id}")
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    return {"erro": "não encontrada"}          # problema?

    #Apesar do Erro ele ira devolver status 200, o que pode confundir o usuario.

@app.post("/reservas")
async def criar_reserva(reserva: ReservaInput):
    # problema?
    nova = {"id": len(reservas) + 1, **reserva.model_dump(), "ativa": True}
    reservas.append(nova)
    return nova

    #Ele está aceitando campos vazios e valores negativos como por exemplo eu posso colocar meu nome vazio e o número de pessoas como negativo.

@app.delete("/reservas/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            r["ativa"] = False
            return {"mensagem": "cancelada"}
    # problema?

    #Ele não avisa erros em caso por exemplo da reserva não existir, e nem fala qual reserva foi apagada então se você errar seu ID vc estará apagando outra reserva sem nem saber.


@app.get("/reservas")
async def listar_reservas(apenas_ativas: bool = False):
    if apenas_ativas:
        return [r for r in reservas if r["ativa"] == "true"]  # problema?
    return reservas
# "True" KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK