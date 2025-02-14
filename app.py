import streamlit as st
from utils import chatbot, text as txt
from streamlit_chat import message

def main():
    st.set_page_config(page_title='B3 - AI Prospects Analysis', page_icon=':moneybag:')
    st.header('Conversar...')

    # Inicializa o estado da conversa na sessão do Streamlit
    if "conversational" not in st.session_state:
        st.session_state.conversational = None

    # Verifica se o vector_store foi carregado no session_state
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.subheader('Arquivos carregados')

        pdf_uploaded = st.file_uploader('Carregue seus Arquivos PDF', accept_multiple_files=True)

        if st.button('Adicionar Arquivo Processado') and pdf_uploaded:
            with st.spinner("Processando arquivo..."):
                all_files_text = txt.process_text(pdf_uploaded)
                chunks = txt.create_text_chunks(text=all_files_text, chunks=1000, overlap=200)

                vector_store = chatbot.create_vectorstore(chunks=chunks)
                st.session_state.vector_store = vector_store
                
                st.session_state.conversational = chatbot.create_conversation_chain(vectorstore=vector_store)

            st.success("Arquivo processado com sucesso! Agora você pode fazer perguntas.")
            
            
    user_question = st.text_input("Digite sua pergunta e pressione Enter")

    if user_question:
        if st.session_state.conversational is not None and st.session_state.vector_store is not None:
            
            # **🔹 Exibir mensagens anteriores do chat**
            for i, (question, answer) in enumerate(st.session_state.messages):
                message(question, is_user=True, key=f"user_{i}")
                message(answer, is_user=False, key=f"bot_{i}")
            

            chat_history = [(q, a) for q, a in st.session_state.messages]  # Histórico formatado

            response = st.session_state.conversational({'question': user_question, 'chat_history': chat_history})

            # **Salvar pergunta e resposta no histórico**
            st.session_state.messages.append((user_question, response['answer']))
            
            # **Atualizar interface do chat com novas mensagens**
            message(user_question, is_user=True, key=f"user_{len(st.session_state.messages)}")
            message(response['answer'], is_user=False, key=f"bot_{len(st.session_state.messages)}")
            
        
if __name__ == '__main__':
    main()
