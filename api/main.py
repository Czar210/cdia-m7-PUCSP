from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers import pratos, bebidas, pedidos, reservas, predict

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
        }
    )


@app.get("/")
async def root():
    return {"mensagem": "Bem-vindo ao Bella Tavola!"}


app.include_router(pratos.router, prefix="/pratos", tags=["Pratos"])
app.include_router(bebidas.router, prefix="/bebidas", tags=["Bebidas"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(predict.router, prefix="/ml", tags=["ML"])


@app.get("/health", tags=["Health"])
async def health():
    model_status = "unavailable"
    try:
        from routers.predict import get_model
        get_model()
        model_status = "loaded"
    except Exception:
        model_status = "error"
    return {"api": "ok", "model": model_status}
