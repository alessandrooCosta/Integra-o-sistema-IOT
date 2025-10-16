from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from soap_client import criar_ordem_servico

app = FastAPI()
# Ajuste: O Uvicorn está sendo executado DE DENTRO da pasta 'api',
# então o caminho correto é apenas 'templates' (assumindo que há uma pasta 'templates' dentro de 'api').
templates = Jinja2Templates(directory="templates")

LIMITE_NIVEL = 5.0
leituras = []  # memória (MVP)

# ----------------------------------------------------------------------
# ROTA SUGERIDA: Redireciona a rota raiz (/) para o Dashboard
# ----------------------------------------------------------------------
@app.get("/")
async def root_redirect():
    """Redireciona o acesso à URL base para o dashboard."""
    # O RedirectResponse garante que ao acessar http://127.0.0.1:8000
    # o usuário é automaticamente enviado para a rota /dashboard.
    return RedirectResponse(url="/dashboard")

# ----------------------------------------------------------------------
# ROTA DE DADOS (POST)
# ----------------------------------------------------------------------
@app.post("/sensor-data")
async def receber_dado_sensor(request: Request):
    """Recebe dados JSON do sensor, armazena em memória e verifica o limite."""
    payload = await request.json()
    nivel = payload.get("nivel")
    local = payload.get("local", "Desconhecido")
    timestamp = payload.get("timestamp", datetime.utcnow().isoformat())

    # Salvar em memória (adiciona o mais novo na frente)
    leituras.insert(0, {"nivel": nivel, "local": local, "timestamp": timestamp})
    if len(leituras) > 20:  # Limita histórico
        leituras.pop()

    # Lógica de negócio: se o nível ultrapassar o limite, cria a ordem de serviço
    if nivel is not None and nivel > LIMITE_NIVEL:
        # Nota: Certifique-se de que a função criar_ordem_servico não está levantando exceções
        criar_ordem_servico(local, nivel, timestamp)

    return JSONResponse({"status": "ok", "nivel": nivel, "local": local})

# ----------------------------------------------------------------------
# ROTA DO DASHBOARD (GET)
# ----------------------------------------------------------------------
@app.get("/dashboard")
async def dashboard(request: Request):
    """Exibe o template HTML do dashboard com os dados e limites atuais."""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "leituras": leituras,
        "limite": LIMITE_NIVEL
    })