import streamlit as st
from utils import chatbot, text as txt
from streamlit_chat import message
from utils.dictionaries import embedding_models, llm_models, embedding_models_carregados, tipo_chunk

from utils.load_vectorstores import load_vector_store
import os
os.environ["GROQ_API_KEY"] = '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'


# Carrega uma única vez os índices e os armazena no estado da sessão
if "preloaded_vector_store" not in st.session_state:
    st.session_state.preloaded_vector_store = load_vector_store()

st.set_page_config(page_title='B3 - AI Prospects Analysis', page_icon=':moneybag:', layout='wide')



def main():
    st.markdown("""
        <style>
        .main-container {
            background-color: #212121;
            color: #e0e0e0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .sidebar .block-container {
            background-color: #2c2c2c;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .stButton>button {
            background-color: #e53935;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #d32f2f;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            font-size: 16px;
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #e53935;
            padding: 8px;
        }
        .stSelectbox select {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #e53935;
            border-radius: 8px;
            padding: 8px;
        }
        .stSlider>div>div>input {
            background-color: #2c2c2c;
            border-radius: 8px;
            color: #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title(':moneybag: B3 - AI Prospects Analysis')
    st.header('Converse com a IA de análise financeira')

    if "conversational" not in st.session_state:
        st.session_state.conversational = None

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
        
    if "new_vector_store" not in st.session_state:
        st.session_state.new_vector_store = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.markdown('<div class="sidebar block-container">', unsafe_allow_html=True)
        if st.button('Limpar Conversas'):
            st.session_state.messages = []
            
        st.subheader('⚙️ Configurações')
        own_docs_search = st.toggle('Tipo de resposta')
        if own_docs_search:
            st.success('Obtendo Respostas somente do documento a ser carregado')
        else:
            st.success('Obtendo Respostas do dataset pre carregado')
        
        # Seleção do modelo de embedding
        selected_embedding = st.selectbox("🔍 Modelo de Embedding para transformação de novos documentos:", options=list(embedding_models.keys()), index=0)
        selected_llm = st.selectbox("🤖 Modelos de LLMS Disponiveis para Consulta:", options=list(llm_models.keys()), index=0)
        
        embeddings_carregados = st.selectbox("🔍 Embeddings Pré-carregados:", options=list(embedding_models_carregados.keys()), index=0)
        escolher_chunks_carregados = st.selectbox("🔍 Divisões Processadas Disponíveis:", options=list(tipo_chunk.keys()), index=0)
        
        chunk_size = st.slider("📏 Tamanho de Chunks para Processar novos Arquivos:", min_value=100, max_value=5000, value=1000, step=100)
        overlap = st.slider("🔄 Tamanho de Sobreposição (Overlap) entre Chunks:", min_value=0, max_value=1000, value=200, step=50)
        search_slider = st.slider("🔍 Quantidade de Documentos Relevantes Retornados:", min_value=1, max_value=15, value=1, step=1)
        
        
        # Seleciona o vetor pré-carregado de acordo com o embedding escolhido
        preloaded = st.session_state.preloaded_vector_store
        
        if embeddings_carregados == 'Embedding 1':
            vector_list = preloaded['faiss_vector1']
        elif embeddings_carregados == 'Embedding 2':
            vector_list = preloaded['faiss_vector2']
        elif embeddings_carregados == 'Embedding 3':
            vector_list = preloaded['faiss_vector3']
            
        if vector_list is None:
            st.warning("⚠️ Nenhum vetor carregado. O chatbot pode não funcionar corretamente.")
        else:
            st.session_state.vector_store = vector_list
        
        st.subheader('📂 Arquivos carregados')
        pdf_uploaded = st.file_uploader('📥 Carregue seus PDFs', accept_multiple_files=True)

        if st.button('🚀 Processar Arquivo') and pdf_uploaded:
            with st.spinner("🛠️ Processando arquivo..."):
                
                all_files_text = txt.process_text(pdf_uploaded)
                
                if all_files_text != '':
                    chunks = txt.create_text_chunks(text=all_files_text, chunks=chunk_size, overlap=overlap)
                
                    vector_store = chatbot.create_vectorstore(chunks=chunks, model=embedding_models[selected_embedding])
                    st.session_state.new_vector_store = vector_store
                
                    st.success("✅ Arquivo processado com sucesso! Agora você pode fazer perguntas.")
                
        else:
            st.error("Adicione algum arquivo para ser processado!")

        st.success("✅ Chatbot inicializado com o vetor pré-carregado!")
        st.markdown('</div>', unsafe_allow_html=True)
             
    
    user_question = st.text_input("💬 Digite sua pergunta e pressione Enter")
    if user_question:
        for i, (question, answer) in enumerate(st.session_state.messages):
            message(question, is_user=True, key=f"user_{i}")
            message(answer, is_user=False, key=f"bot_{i}")
        
        chat_history = [(q, a) for q, a in st.session_state.messages]
        
        if not own_docs_search:
            st.session_state.conversational = chatbot.create_conversation_chain(vectorstore=st.session_state.vector_store, model_name=llm_models[selected_llm], search_model_kargs=search_slider, chunk_type=tipo_chunk[escolher_chunks_carregados])
        else:
            if st.session_state.new_vector_store != None:
                st.session_state.conversational = chatbot.create_conversation_chain(vectorstore=st.session_state.new_vector_store, model_name=llm_models[selected_llm], search_model_kargs=search_slider, chunk_type=tipo_chunk[escolher_chunks_carregados])
            else:
                st.error("Processe um Arquivo primeiro para usar a função de responder somente a texto carregado")
        
        response = st.session_state.conversational({'question': user_question, 'chat_history': chat_history})
        
        st.session_state.messages.append((user_question, response['answer']))
        
        message(user_question, is_user=True, key=f"user_{len(st.session_state.messages)}")
        message(response['answer'], is_user=False, key=f"bot_{len(st.session_state.messages)}")

    
    st.markdown('</div>', unsafe_allow_html=True)
            
if __name__ == '__main__':
    main()
