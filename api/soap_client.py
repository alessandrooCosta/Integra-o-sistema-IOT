# api/soap_client.py
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Endpoint do seu servidor de teste
HXGN_ENDPOINT = "http://192.168.15.9:7575/axis/services/EWSConnector"

# Credenciais locais
HXGN_USER = "ACOSTA"
HXGN_PASS = "Assettec@2025"

# Namespaces SOAP e da função
SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"
FUNC_NS = "http://schemas.datastream.net/MP_functions/MP0102_001"  # Função de criação de OS

# Campos fixos de teste — depois podemos torná-los dinâmicos
TIPO_OS = "Breakdown"
EQUIPAMENTO = "AR-001"
DEPARTAMENTO = "*"
STATUS = "R"
ORGANIZACAO = "ORG01"

def criar_ordem_servico(local: str, nivel: float, timestamp: str):
    descricao = f"⚠️ Alerta de nível de água em {local}"
    notas = f"Nível: {nivel} mm - Data/Hora: {timestamp}"

    envelope = f"""
    <soapenv:Envelope xmlns:soapenv="{SOAP_NS}" xmlns:mp="{FUNC_NS}">
       <soapenv:Header/>
       <soapenv:Body>
          <mp:MP0102_CreateWorkOrder>
             <mp:workorder>
                <mp:organization>{ORGANIZACAO}</mp:organization>
                <mp:department>{DEPARTAMENTO}</mp:department>
                <mp:equipment>{EQUIPAMENTO}</mp:equipment>
                <mp:wotype>{TIPO_OS}</mp:wotype>
                <mp:description>{descricao}</mp:description>
                <mp:notes>{notas}</mp:notes>
                <mp:status>{STATUS}</mp:status>
             </mp:workorder>
          </mp:MP0102_CreateWorkOrder>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "MP0102_CreateWorkOrder"
    }

    try:
        print("📡 Enviando requisição SOAP para EWSConnector local...")
        response = requests.post(
            HXGN_ENDPOINT,
            data=envelope.encode("utf-8"),
            headers=headers,
            auth=HTTPBasicAuth(HXGN_USER, HXGN_PASS),
            timeout=15
        )
        print(f"📬 Status: {response.status_code}")
        print(f"📝 Resposta SOAP:\n{response.text[:600]}")

        if response.status_code == 200 and "<returnCode>0</returnCode>" in response.text:
            print("✅ OS criada com sucesso no EAM!")
        else:
            print("⚠️ Falha ao criar OS — verifique a resposta acima.")

    except Exception as e:
        print(f"❌ Erro na integração SOAP: {e}")
