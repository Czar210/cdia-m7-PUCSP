from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from models.bebida import BebidaInput, BebidaOutput

router = APIRouter()

bebidas = [
    {"id": 1, "nome": "Aperol Spritz", "categoria": "drink", "preco": 32.0, "volume_ml": 250, "ingredientes": ["Aperol", "prosecco", "água com gás"], "disponivel": True},
    {"id": 2, "nome": "Negroni", "categoria": "drink", "preco": 35.0, "volume_ml": 100, "ingredientes": ["gin", "vermute tinto", "Campari"], "disponivel": True},
    {"id": 3, "nome": "Vinho Chianti (Taça)", "categoria": "vinho", "preco": 38.0, "volume_ml": 150, "ingredientes": ["uva Sangiovese", "frutas vermelhas"], "disponivel": True},
    {"id": 4, "nome": "Água Mineral", "categoria": "agua", "preco": 6.0, "volume_ml": 310, "ingredientes": ["água mineral"], "disponivel": True},
    {"id": 5, "nome": "Coca-Cola Lata", "categoria": "refrigerante", "preco": 8.0, "volume_ml": 350, "ingredientes": ["refrigerante de cola"], "disponivel": True},
    {"id": 6, "nome": "Suco de Laranja", "categoria": "suco", "preco": 12.0, "volume_ml": 300, "ingredientes": ["laranja natural"], "disponivel": True},
    {"id": 7, "nome": "Cerveja Peroni", "categoria": "cerveja", "preco": 22.0, "volume_ml": 330, "ingredientes": ["malte de cevada", "lúpulo"], "disponivel": True},
    {"id": 8, "nome": "Limoncello", "categoria": "digestivo", "preco": 18.0, "volume_ml": 50, "ingredientes": ["limão siciliano", "álcool", "açúcar"], "disponivel": True},
    {"id": 9, "nome": "Café Espresso", "categoria": "cafe", "preco": 8.0, "volume_ml": 30, "ingredientes": ["grãos arábica", "água"], "disponivel": True}
]


@router.get("/", tags=["Bebidas"])
async def listar_bebidas(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    disponivel: Optional[bool] = None
):
    resultado = bebidas
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    if disponivel is not None:
        resultado = [p for p in resultado if p.get('disponivel') == disponivel]
    return resultado


@router.get("/{bebida_id}", tags=["Bebidas"])
async def buscar_bebida(bebida_id: int, disponivel: Optional[bool] = None):
    bebida_encontrada = None
    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            bebida_encontrada = bebida
            break
    if not bebida_encontrada:
        raise HTTPException(status_code=404, detail="Bebida não encontrada")
    if disponivel is not None:
        if bebida_encontrada.get("disponivel") != disponivel:
            raise HTTPException(status_code=404, detail="Bebida encontrada, mas não tem versão vegetariana")
    return bebida_encontrada


@router.get("/{bebida_id}/detalhes", tags=["Bebidas"])
async def detalhes_bebida(bebida_id: int, incluir_ingredientes: bool = False):
    for bebida in bebidas:
        if bebida["id"] == bebida_id:
            if incluir_ingredientes:
                return bebida
            else:
                bebida_resumo = {k: v for k, v in bebida.items() if k != "ingredientes"}
                return bebida_resumo
    raise HTTPException(status_code=404, detail="Bebida não encontrada")


@router.post("/input", response_model=BebidaOutput, status_code=201, tags=["Bebidas"])
async def criar_bebida(bebida: BebidaInput):
    novo_id = max((p["id"] for p in bebidas), default=0) + 1
    nova_bebida = {"id": novo_id, **bebida.model_dump()}
    nova_bebida["criado_em"] = datetime.now().isoformat()
    bebidas.append(nova_bebida)
    return nova_bebida


@router.post("/{bebida_id}/aplicar_desconto", tags=["Bebidas"])
async def aplicar_desconto(bebida_id: int, percentual: float):
    bebida = next((b for b in bebidas if b["id"] == bebida_id), None)
    if not bebida:
        raise HTTPException(status_code=404, detail="Bebida não encontrada")
    if percentual <= 0 or percentual > 50:
        raise HTTPException(status_code=400, detail="Percentual de desconto deve estar entre 1% e 50%")
    if not bebida.get("disponivel"):
        raise HTTPException(status_code=400, detail="Não é possível aplicar desconto em bebida indisponível")
    bebida["preco"] = bebida["preco"] * (1 - percentual / 100)
    return bebida


@router.put("/{bebida_id}/disponibilidade", tags=["Bebidas"])
async def atualizar_disponibilidade(bebida_id: int, disponivel: bool):
    bebida = next((b for b in bebidas if b["id"] == bebida_id), None)
    if not bebida:
        raise HTTPException(status_code=404, detail="Bebida não encontrada")
    bebida["disponivel"] = disponivel
    return bebida
