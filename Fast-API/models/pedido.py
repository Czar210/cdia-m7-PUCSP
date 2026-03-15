from pydantic import BaseModel, Field
from typing import Optional


class Pedido(BaseModel):
    prato_id: int
    bebida_id: Optional[int] = None
    quantidade_prato: int = Field(gt=0, description="Quantidade do prato, deve ser positiva")
    quantidade_bebida: Optional[int] = Field(default=None, gt=0, description="Quantidade da bebida, deve ser positiva se fornecida")
    descricao: Optional[str] = Field(default=None, max_length=500)
