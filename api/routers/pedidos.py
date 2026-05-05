from fastapi import APIRouter, HTTPException
from typing import Optional
from models.pedido import Pedido
from routers.pratos import pratos
from routers.bebidas import bebidas

router = APIRouter()
pedidos = []


@router.post("/", tags=["Pedidos"])
async def criar_pedido(pedido: Pedido, id_prato: int, id_bebida: Optional[int] = None, quantidade_prato: int = 1, quantidade_bebida: Optional[int] = None):
    prato = next((p for p in pratos if p["id"] == id_prato), None)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    if not prato.get("disponivel"):
        raise HTTPException(status_code=400, detail="Prato indisponível")

    if id_bebida is not None:
        bebida = next((b for b in bebidas if b["id"] == id_bebida), None)
        if not bebida:
            raise HTTPException(status_code=404, detail="Bebida não encontrada")
        if not bebida.get("disponivel"):
            raise HTTPException(status_code=400, detail="Bebida indisponível")

    return {"message": "Pedido criado com sucesso", "pedido": pedido}
