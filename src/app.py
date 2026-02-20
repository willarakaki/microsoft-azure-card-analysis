import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analyze_credit_card

def configure_interface():
    st.title("Upload de arquivos - Azure - Fake Docs")
    file = st.file_uploader("Upload de arquivos de imagem", type=["jpg", "png", "jpeg"])
    
    if file is not None:
        file_name = file.name
        
        blob_url = upload_blob(file_name, file)
        
        with st.spinner("Conectando ao Azure e analisando o cartão... Por favor, aguarde."):
        
            if blob_url:
                st.toast(f"Imagem enviada com sucesso!")
                credit_card_info = analyze_credit_card(blob_url)
                show_image_and_validation(credit_card_info, file)
            else:
                st.error(f"Erro ao enviar o arquivo {file_name} para o Azure Blob Storage")
            

def show_image_and_validation(credit_card_info, file):
    st.image(file, caption="Imagem enviada", width='stretch')
    st.write("Resultado da validação:")
    
    if credit_card_info and credit_card_info.get("card_name"):
        st.markdown("<h1 style='color: green;'>Cartão de crédito validado</h1>", unsafe_allow_html=True)
        
        st.write(f"Nome do cartão: {credit_card_info.get('card_name') or 'Não identificado'}")
        st.write(f"Número do cartão: {credit_card_info.get('card_number') or 'Não identificado'}")
        st.write(f"Bandeira: {credit_card_info.get('card_brand') or 'Não identificada'}")
        st.write(f"CVV: {credit_card_info.get('cvv') or 'Não identificado'}")
        st.write(f"Data de emissão: {credit_card_info.get('issue_date') or 'Não identificada'}")
        st.write(f"Data de validade: {credit_card_info.get('expiration_date') or 'Não identificada'}")
        
    else:
        st.markdown("<h1 style='color: red;'>Cartão de crédito não validado</h1>", unsafe_allow_html=True)
        st.write("Não foi possível identificar informações suficientes na imagem.")
        
if __name__ == "__main__":
    configure_interface()