import requests
from datetime import datetime

HXGN_ENDPOINT = "http://192.168.15.9:7575/axis/services/EWSConnector"

HXGN_USER = "ACOSTA"
HXGN_PASS = "Assettec@2025"
HXGN_ORG = "ASSET-TEST"

def criar_ordem_servico(local: str, nivel: float, timestamp: str):
    """
    Cria uma Ordem de Serviço no HxGN EAM via MP0023_AddWorkOrder_001
    compatível com schema base (sem campos de nota/comentário).
    """
    descricao_curta = f"Alerta: nível de água {nivel}mm em {local}"[:80]

    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:mp="http://schemas.datastream.net/MP_functions/MP0023_001"
        xmlns:wo="http://schemas.datastream.net/MP_entities/WorkOrder_001"
        xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/04/secext"
        xmlns:mf="http://schemas.datastream.net/MP_fields">

        <soapenv:Header>
            <wsse:Security>
                <wsse:UsernameToken>
                    <wsse:Username>{HXGN_USER}</wsse:Username>
                    <wsse:Password>{HXGN_PASS}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
            <Organization xmlns="http://schemas.datastream.net/headers">{HXGN_ORG}</Organization>
        </soapenv:Header>

        <soapenv:Body>
            <mp:MP0023_AddWorkOrder_001 verb="Add" noun="WorkOrder" version="001" callname="AddWorkOrder">
                <wo:WorkOrder>

                    <mf:WORKORDERID auto_generated="true">
                        <mf:JOBNUM></mf:JOBNUM>
                        <mf:ORGANIZATIONID entity="User">
                            <mf:ORGANIZATIONCODE>{HXGN_ORG}</mf:ORGANIZATIONCODE>
                        </mf:ORGANIZATIONID>
                        <mf:DESCRIPTION>{descricao_curta}</mf:DESCRIPTION>
                    </mf:WORKORDERID>

                    <mf:STATUS entity="User">
                        <mf:STATUSCODE>R</mf:STATUSCODE>
                        <mf:DESCRIPTION>Ready</mf:DESCRIPTION>
                    </mf:STATUS>

                    <mf:EQUIPMENTID>
                        <mf:EQUIPMENTCODE>AR-001</mf:EQUIPMENTCODE>
                        <mf:ORGANIZATIONID entity="Organization">
                            <mf:ORGANIZATIONCODE>*</mf:ORGANIZATIONCODE>
                        </mf:ORGANIZATIONID>
                    </mf:EQUIPMENTID>

                    <mf:DEPARTMENTID>
                        <mf:DEPARTMENTCODE>*</mf:DEPARTMENTCODE>
                        <mf:ORGANIZATIONID entity="Group">
                            <mf:ORGANIZATIONCODE>{HXGN_ORG}</mf:ORGANIZATIONCODE>
                        </mf:ORGANIZATIONID>
                    </mf:DEPARTMENTID>

                    <mf:TYPE entity="User">
                        <mf:TYPECODE>BRKD</mf:TYPECODE>
                        <mf:DESCRIPTION>Emergência Automática</mf:DESCRIPTION>
                    </mf:TYPE>

                    <mf:FIXED></mf:FIXED>

                </wo:WorkOrder>
            </mp:MP0023_AddWorkOrder_001>
        </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "AddWorkOrder"
    }

    try:
        print("📡 Enviando requisição SOAP para EAM.")
        response = requests.post(
            HXGN_ENDPOINT,
            data=envelope.encode("utf-8"),
            headers=headers,
            timeout=20
        )

        print(f"📬 Status HTTP: {response.status_code}")

        if response.status_code == 200 and "<returnCode>0</returnCode>" in response.text:
            print("✅ Ordem de Serviço criada com sucesso no EAM!")
        elif "faultstring" in response.text.lower():
            print("❌ Falha SOAP detectada. Verifique campos obrigatórios.")
        else:
            print("⚠️ Requisição enviada, mas sem confirmação de sucesso.")

    except Exception as e:
        print(f"🚨 Erro durante integração SOAP: {e}")
