from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from models.prato import PratoInput, PratoOutput

router = APIRouter()

pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "ingredientes": ["molho de tomate (vermelho)", "muçarela de búfala",  "manjericão fresco (verde)", "azeite de oliva", "rodelas de tomate fresco"], "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "ingredientes":["espaguete", "guanciale ", "gemas de ovos", "queijo pecorino romano", "pimenta-do-reino", "sal"], "disponivel": True},
    {"id": 3, "nome": "Lasanha Bolonhesa", "categoria": "massa", "preco": 58.0, "ingredientes":["massa de lasanha", "carne moída", "molho de tomate", "leite", "manteiga", "farinha de trigo", "queijo muçarela", "presunto", "queijo parmesão", "cebola", "alho", "azeite", "sal", "pimenta-do-reino", "noz-moscada"], "disponivel": False},
    {"id": 4, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0,"ingredientes": ["queijo mascarpone", "biscoitos savoiardi", "ovos", "açúcar", "café expresso", "cacau em pó", "vinho marsala"], "disponivel": True},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza", "preco": 49.0, "ingredientes": ["massa", 'molho de tomate', 'queijo muçarela', 'presunto cozido', 'alcachofras', 'cogumelos', 'azeitonas pretas'], "disponivel": False},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 24.0, "ingredientes": ['creme', 'açúcar', 'baunilha', 'gelatina'], "disponivel": True}
]


@router.get("/", tags=["Pratos"])
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    disponivel: Optional[bool] = None
):
    resultado = pratos
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    if disponivel is not None:
        resultado = [p for p in resultado if p.get('disponivel') == disponivel]
    return resultado


@router.get("/{prato_id}", tags=["Pratos"])
async def buscar_prato(prato_id: int, disponivel: Optional[bool] = None):
    prato_encontrado = None
    for prato in pratos:
        if prato["id"] == prato_id:
            prato_encontrado = prato
            break
    if not prato_encontrado:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    if disponivel is not None:
        if prato_encontrado.get("disponivel") != disponivel:
            raise HTTPException(
                status_code=404,
                detail="Prato encontrado, mas não tem versão vegetariana"
            )
    return prato_encontrado


@router.get("/{prato_id}/detalhes", tags=["Pratos"])
async def detalhes_prato(prato_id: int, incluir_ingredientes: bool = False):
    for prato in pratos:
        if prato["id"] == prato_id:
            if incluir_ingredientes:
                return prato
            else:
                prato_resumo = {k: v for k, v in prato.items() if k != "ingredientes"}
                return prato_resumo
    raise HTTPException(status_code=404, detail="Prato não encontrado")


@router.post("/input", response_model=PratoOutput, status_code=201, tags=["Pratos"])
async def criar_prato(prato: PratoInput):
    novo_id = max((p["id"] for p in pratos), default=0) + 1
    novo_prato = {"id": novo_id, **prato.model_dump()}
    novo_prato["criado_em"] = datetime.now().isoformat()
    pratos.append(novo_prato)
    return novo_prato


@router.post("/{prato_id}/aplicar_desconto", tags=["Pratos"])
async def aplicar_desconto(prato_id: int, percentual: float):
    prato = next((p for p in pratos if p["id"] == prato_id), None)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    if percentual <= 0 or percentual > 50:
        raise HTTPException(status_code=400, detail="Percentual de desconto deve estar entre 1% e 50%")
    if not prato.get("disponivel"):
        raise HTTPException(status_code=400, detail="Não é possível aplicar desconto em prato indisponível")
    prato["preco"] = prato["preco"] * (1 - percentual / 100)
    return prato


@router.put("/{prato_id}/disponibilidade", tags=["Pratos"])
async def atualizar_disponibilidade(prato_id: int, disponivel: bool):
    prato = next((p for p in pratos if p["id"] == prato_id), None)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    prato["disponivel"] = disponivel
    return prato
