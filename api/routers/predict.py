from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()

REPO_ID = None  # set via env or override; None = use local MODEL_PATH
_model = None


def get_model():
    global _model
    if _model is None:
        import os
        from model_utils import load_model

        repo = os.environ.get("HF_REPO_ID", REPO_ID)
        _model = load_model(repo_id=repo)
    return _model


class CreditInput(BaseModel):
    renda_mensal: float = Field(gt=0, description="Renda mensal em reais")
    divida_atual: float = Field(ge=0, description="Dívida atual em reais")
    historico_pagamentos: int = Field(ge=0, le=100, description="Score de histórico (0-100)")
    idade: int = Field(ge=18, le=120, description="Idade do solicitante")
    num_dependentes: int = Field(ge=0, le=20, description="Número de dependentes")


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str = "1.0.0"


@router.post("/predict", response_model=PredictOutput)
async def predict(data: CreditInput):
    model = get_model()
    features = np.array([[
        data.renda_mensal,
        data.divida_atual,
        data.historico_pagamentos,
        data.idade,
        data.num_dependentes,
    ]])
    pred = int(model.predict(features)[0])
    proba = float(model.predict_proba(features)[0][1])
    label = "inadimplente" if pred == 1 else "adimplente"
    return PredictOutput(prediction=pred, probability=round(proba, 4), label=label)
