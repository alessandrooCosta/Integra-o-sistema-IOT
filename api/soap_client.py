# api/soap_client.py
import requests
from requests.auth import HTTPBasicAuth

# Exemplo de endpoint SOAP (ajuste para o seu ambiente)
HXGN_ENDPOINT = "https://seu-servidor-eam.com/ws/MP0102_CreateWorkOrder"

# Credenciais do EAM
HXGN_USER = "ACOSTA"
HXGN_PASS = "Asset@25"

# Namespace padrão do HxGN EAM
SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"
EAM_NS = "http://ws.eam.infor.com/"

def criar_ordem_servico(local: str, nivel: float, timestamp: str):
    """
    Chama o serviço SOAP do HxGN EAM para criar uma Ordem de Serviço.
    """
    descricao = f"⚠️ Nível de água alto detectado em {local}"
    notas = f"Nível: {nivel} mm | Horário: {timestamp}"

    envelope = f"""
    <soapenv:Envelope xmlns:soapenv="{SOAP_NS}" xmlns:ws="{EAM_NS}">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:MP0102_CreateWorkOrder>
             <ws:workorder>
                <ws:organization>ORG01</ws:organization>
                <ws:department>{local}</ws:department>
                <ws:wotype>INSPEC</ws:wotype>
                <ws:description>{descricao}</ws:description>
                <ws:notes>{notas}</ws:notes>
                <ws:status>R</ws:status>
             </ws:workorder>
          </ws:MP0102_CreateWorkOrder>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "MP0102_CreateWorkOrder"
    }

    try:
        print("📡 Enviando requisição SOAP real para HxGN EAM...")
        response = requests.post(
            HXGN_ENDPOINT,
            data=envelope.encode("utf-8"),
            headers=headers,
            auth=HTTPBasicAuth(HXGN_USER, HXGN_PASS),
            verify=False  # ⚠️ Apenas se o servidor tiver certificado self-signed
        )

        print(f"📬 Status: {response.status_code}")
        print(f"📝 Resposta SOAP:\n{response.text[:500]}")  # mostra parte inicial
    except Exception as e:
        print(f"❌ Erro na integração SOAP: {e}")
