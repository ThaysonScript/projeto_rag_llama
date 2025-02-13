import streamlit as st


def main():
    st.set_page_config(page_title='B3 - AI Prospects Analisys', page_icon=':moneybag:')
    
    with st.sidebar:
        st.subheader('Arquivos carregados')
        
        pdf_uploaded = st.file_uploader('Carregue seus Arquivos PDF', accept_multiple_files=True)
        
        print(pdf_uploaded)
        
        if st.button('Adicionar Arquivo Processado'):
            pass
    
    
if __name__ == '__main__':
    main()