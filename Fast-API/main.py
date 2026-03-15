from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional
from datetime import datetime

# import models from models/ package (refactored for Block 3)
from models.prato import PratoInput, PratoOutput
from models.bebida import BebidaInput, BebidaOutput
from models.pedido import Pedido
from models.reserva import ReservaInput, ReservaOutput



class Prato(BaseModel):
    nome: str = Field(min_length=3, max_length=100, description="Nome do prato")
    categoria: str = Field(description="Categoria do prato")
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True

class Pedido(BaseModel):   
    prato_id: int
    bebida_id: Optional[int] = None
    quantidade_prato: int = Field(gt=0, description="Quantidade do prato, deve ser positiva")
    quantidade_bebida: Optional[int] = Field(default=None, gt=0, description="Quantidade da bebida, deve ser positiva se fornecida")
    descricao: Optional[str] = Field(default=None, max_length=500)

class PratoInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100, description="Nome do prato")
    categoria: str = Field(pattern="^(pizza|massa|sobremesa|entrada|salada)$")
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True
    preco_promocional: Optional[float] = Field(default=None, gt=0)


    @field_validator("preco_promocional")
    @classmethod
    def validar_preco_promocional(cls, v, info):
        if v is None:
            return v
        if "preco" not in info.data:
            return v

        preco_original = info.data["preco"]

        if v >= preco_original:
            raise ValueError("Preço promocional deve ser menor que o preço original")

        desconto = (preco_original - v) / preco_original
        if desconto > 0.5:
            raise ValueError("Desconto não pode ser maior que 50% do preço original")

        return v


class PratoOutput(BaseModel):
    id: int
    nome: str = Field(min_length=3, max_length=100, description="Nome do prato")
    categoria: str = Field(pattern="^(pizza|massa|sobremesa|entrada|salada)$")
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True
    criado_em: str = Field(default_factory=lambda: datetime.now().isoformat())
    preco_promocional: Optional[float] = Field(default=None, gt=0)

    @field_validator("preco_promocional")
    @classmethod
    def validar_preco_promocional(cls, v, info):
        if v is None:
            return v
        if "preco" not in info.data:
            return v

        preco_original = info.data["preco"]

        if v >= preco_original:
            raise ValueError("Preço promocional deve ser menor que o preço original")

        desconto = (preco_original - v) / preco_original
        if desconto > 0.5:
            raise ValueError("Desconto não pode ser maior que 50% do preço original")

        return v

class BebidaInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100, description="Nome da bebida")
    categoria: str = Field(pattern="^(vinho|agua|refrigerante|suco|cerveja|drink|digestivo|cafe)$")
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True
    preco_promocional: Optional[float] = Field(default=None, gt=0)

    @field_validator("preco_promocional")
    @classmethod
    def validar_preco_promocional(cls, v, info):
        if v is None:
            return v
        if "preco" not in info.data:
            return v

        preco_original = info.data["preco"]

        if v >= preco_original:
            raise ValueError("Preço promocional deve ser menor que o preço original")

        desconto = (preco_original - v) / preco_original
        if desconto > 0.5:
            raise ValueError("Desconto não pode ser maior que 50% do preço original")

        return v

class BebidaOutput(BaseModel):
    id: int
    nome: str = Field(min_length=3, max_length=100, description="Nome da bebida")
    categoria: str = Field(pattern="^(vinho|agua|refrigerante|suco|cerveja|drink|digestivo|cafe)$")
    preco: float = Field(gt=0, description="Preço em reais, deve ser positivo")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True
    criado_em: str = Field(default_factory=lambda: datetime.now().isoformat())
    preco_promocional: Optional[float] = Field(default=None, gt=0)

    @field_validator("preco_promocional")
    @classmethod
    def validar_preco_promocional(cls, v, info):
        if v is None:
            return v
        if "preco" not in info.data:
            return v

        preco_original = info.data["preco"]

        if v >= preco_original:
            raise ValueError("Preço promocional deve ser menor que o preço original")

        desconto = (preco_original - v) / preco_original
        if desconto > 0.5:
            raise ValueError("Desconto não pode ser maior que 50% do preço original")

        return v


app = FastAPI(
    title="Bella Tavola API",
    description="API do restaurante Bella Tavola",
    version="1.0.2"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detalhes = []
    for e in errors:
        loc = ".".join(str(loc) for loc in e.get("loc", []))
        detalhes.append({"loc": loc, "msg": e.get("msg")})
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Validation Error",
            "status": 422,
            "path": request.url.path,
            "detalhes": detalhes,

        # include routers
        from routers import pratos, bebidas, pedidos, reservas

        app.include_router(pratos.router, prefix="/pratos", tags=["Pratos"])
        app.include_router(bebidas.router, prefix="/bebidas", tags=["Bebidas"])
        app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
        app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
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


@app.get("/reservas")
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


@app.get("/reservas/mesa/{numero}")
async def reservas_por_mesa(numero: int):
    return [r for r in reservas if r["mesa"] == numero]


@app.get("/reservas/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@app.delete("/reservas/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            if not r["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")

