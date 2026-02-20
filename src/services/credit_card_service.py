from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config
import streamlit as st

def limpar_numeros(numero):
    if not numero:
        return None
    return numero.replace(" ", "").replace("-", "")

def identificar_bandeira(numero_cartao):

    if not numero_cartao:
        return None

    numero_limpo = limpar_numeros(numero_cartao)
    
    if numero_limpo.startswith("4"):
        return "Visa"
    elif numero_limpo.startswith("5"):
        return "Mastercard"
    elif numero_limpo.startswith(("34", "37")):
        return "American Express"
    else:
        return "Desconhecida"
    
def validar_numero_cartao(numero):
    
    numero_limpo = limpar_numeros(numero)
    
    if len(numero_limpo) == 16 or len(numero_limpo) == 15:
        return numero
    else:
        return f"Incompleto - Lido: {numero}"
            

def analyze_credit_card(blob_url):
    try:
        credential = AzureKeyCredential(Config.KEY)
        client = DocumentIntelligenceClient(endpoint=Config.ENDPOINT, credential=credential)

        card_info = client.begin_analyze_document(
            "prebuilt-creditCard", 
            AnalyzeDocumentRequest(url_source=blob_url)
        )
        
        result = card_info.result()
        
        for document in result.documents:
            fields = document.fields
            
            numero_extraido = fields.get("CardNumber", {}).get('content')
            
            bandeira = identificar_bandeira(numero_extraido)
            numero_validado = validar_numero_cartao(numero_extraido)
            
            return {
                "card_name": fields.get("CardHolderName", {}).get('content'),
                "card_number": numero_validado,
                "expiration_date": fields.get("ExpirationDate", {}).get('content'),
                "card_brand": bandeira
            }

    except Exception as e:
        st.error(f"Erro ao analisar o documento: {e}")
        return None