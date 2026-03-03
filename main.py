from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime



class Prato(BaseModel):
    nome: str
    preco: float
    categoria: str

class PratoInput(BaseModel):
    nome: str
    categoria: str
    preco: float
    disponivel: bool = True  


class PratoOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    criado_em: str 

app = FastAPI(
    title="Bella Tavola API",
    description="API do restaurante Bella Tavola",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Ablubleblé",
        "cidade": "São Paulo",
        "especialidade": "Pizza"
    }

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "ingredientes": ["molho de tomate (vermelho)", "muçarela de búfala",  "manjericão fresco (verde)", "azeite de oliva", "rodelas de tomate fresco"], "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "ingredientes":["espaguete", "guanciale ", "gemas de ovos", "queijo pecorino romano", "pimenta-do-reino", "sal"], "disponivel": True},
    {"id": 3, "nome": "Lasanha Bolonhesa", "categoria": "massa", "preco": 58.0, "ingredientes":["massa de lasanha", "carne moída", "molho de tomate", "leite", "manteiga", "farinha de trigo", "queijo muçarela", "presunto", "queijo parmesão", "cebola", "alho", "azeite", "sal", "pimenta-do-reino", "noz-moscada"], "disponivel": False},
    {"id": 4, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0,"ingredientes": ["queijo mascarpone", "biscoitos savoiardi", "ovos", "açúcar", "café expresso", "cacau em pó", "vinho marsala"], "disponivel": True},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza", "preco": 49.0, "ingredientes": ["massa", 'molho de tomate', 'queijo muçarela', 'presunto cozido', 'alcachofras', 'cogumelos', 'azeitonas pretas'], "disponivel": False},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 24.0, "ingredientes": ['creme', 'açúcar', 'baunilha', 'gelatina']}
]



@app.get("/pratos")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    disponivel: Optional[bool] = False
):
    resultado = pratos
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    if disponivel:
        resultado = [p for p in resultado if p['disponivel'] == True]
    return resultado

@app.get("/pratos/{prato_id}")
async def buscar_prato(prato_id: int, disponivel: Optional[bool] = None):
    prato_encontrado = None
    for prato in pratos:
        if prato["id"] == prato_id:
            prato_encontrado = prato
            break
    if not prato_encontrado:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    if disponivel is not None:
        if prato_encontrado["disponivel"] != disponivel:
            raise HTTPException(
                status_code=404, 
                detail="Prato encontrado, mas não tem versão vegetariana"
            )
            
    return prato_encontrado

@app.get("/pratos/{prato_id}/detalhes")
async def detalhes_prato(prato_id: int, incluir_ingredientes: bool = False):
    for prato in pratos:
        if prato["id"] == prato_id:
            if incluir_ingredientes:
                return prato
            else:
                prato = {caracteristica: v for k, v in prato.items() if k != "ingredientes"}
                return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")

@app.post("/pratos/input")
async def criar_prato(prato: PratoInput, descricao: Optional[str] = None, categoria: Optional[str] = None, preco: Optional[float] = 0, disponivel = Optional[Bool] = False):
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {"id": novo_id, **pratoInput.model_dump()}
    if descricao:
        novo_prato['nome'] = descricao
    if categoria:
        novo_prato['categoria'] = categoria
    if preco:
        novo_prato['preco'] = preco
    if disponivel:
        novo_prato['disponivel'] = disponivel
    pratos.append(novo_prato)
    return novo_prato
    pratos.append(novo_prato)
    return novo_prato

@app.post("/pratos/output", response_model=PratoOutput)
async def criar_prato_output(prato: PratoInput):
    from datetime import datetime
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    if descricao:
        novo_prato['nome'] = descricao
    if categoria:
        novo_prato['categoria'] = categoria
    if preco:
        novo_prato['preco'] = preco
    if disponivel:
        novo_prato['disponivel'] = disponivel
    pratos.append(novo_prato)
    return novo_prato