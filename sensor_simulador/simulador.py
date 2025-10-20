# sensor_simulador/simulador.py
import requests
import time
import random
from datetime import datetime

API_URL = "http://localhost:8000/sensor-data"

def enviar_leitura():
    nivel = round(random.uniform(0, 10), 2)  # Simula entre 0 e 10 mm
    payload = {
        "nivel": nivel,
        "local": "Pista 01",
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        r = requests.post(API_URL, json=payload)
        print(f"Enviado: {payload} | Resposta: {r.status_code}")
    except Exception as e:
        print(f"Erro ao enviar leitura: {e}")

if __name__ == "__main__":
    print("🧪 Iniciando simulador de sensor...")
    while True:
        enviar_leitura()
        time.sleep(50)
