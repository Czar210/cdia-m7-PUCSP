from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas = [
    {"id": 1, "mesa": 5, "nome": "Silva", "pessoas": 4, "ativa": True, "data_hora": "2024-12-01T19:00:00", "criada_em": "2024-01-01T00:00:00"},
    {"id": 2, "mesa": 3, "nome": "Costa", "pessoas": 2, "ativa": False, "data_hora": "2024-11-20T20:00:00", "criada_em": "2024-01-01T00:00:00"},
]


@router.post("/", response_model=ReservaOutput, tags=["Reservas"])
async def criar_reserva(reserva: ReservaInput):
    data_reserva = reserva.data_hora.date()
    conflito = any(
        r["mesa"] == reserva.mesa
        and r["ativa"]
        and datetime.fromisoformat(r["data_hora"]).date() == data_reserva
        for r in reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {reserva.mesa} já está reservada para {data_reserva}"
        )
    nova = {
        "id": len(reservas) + 1,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora.isoformat(),
        "ativa": True,
        "criada_em": datetime.now().isoformat()
    }
    reservas.append(nova)
    return nova


@router.get("/", tags=["Reservas"])
async def listar_reservas(data: Optional[str] = None, apenas_ativas: bool = True):
    resultado = reservas
    if apenas_ativas:
        resultado = [r for r in resultado if r["ativa"]]
    if data:
        resultado = [
            r for r in resultado
            if datetime.fromisoformat(r["data_hora"]).date().isoformat() == data
        ]
    return resultado


@router.get("/mesa/{numero}", tags=["Reservas"])
async def reservas_por_mesa(numero: int):
    return [r for r in reservas if r["mesa"] == numero]


@router.get("/{reserva_id}", response_model=ReservaOutput, tags=["Reservas"])
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}", tags=["Reservas"])
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            if not r["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")
