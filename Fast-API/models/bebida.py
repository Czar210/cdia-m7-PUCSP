from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


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
