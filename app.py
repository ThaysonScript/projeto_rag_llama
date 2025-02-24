import os, uuid
import streamlit as st
from streamlit_chat import message
from langchain.prompts import PromptTemplate

from ui.markdowns import (
    end_div,
    styles,
    div
)
from utils import chatbot, text as txt
from utils.load_vectorstores import load_vector_store
from utils.dictionaries import (
    embedding_models,
    llm_models,
    embedding_models_carregados,
    tipo_chunk
)

os.environ["GROQ_API_KEY"] = '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'

st.set_page_config(page_title='B3 - AI Prospects Analysis', page_icon=':moneybag:', layout='wide')
styles()
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

# Carrega os índices pré-carregados na sessão
if "preloaded_vector_store" not in st.session_state:
    st.session_state.preloaded_vector_store = load_vector_store()


def add_new_files(type=''):
    if type == 'llms':
        return st.selectbox("🤖 Modelos de LLMS Disponíveis para Consulta:", options=list(llm_models.keys()), index=0)
    else:
        return st.selectbox("🔍 Modelo de Embedding para transformação de novos documentos:", options=list(embedding_models.keys()), index=0)
    
    
if 'slider_chunk' not in st.session_state:
    st.session_state.slider_chunk = 1000
if 'slider_overlap' not in st.session_state:
    st.session_state.slider_overlap = 200
if 'slider_docs' not in st.session_state:
    st.session_state.slider_docs = 1

def add_new_configs_for_files(type=''):
    if type == 'chunk':
        return st.slider("📏 Tamanho de Chunks para Processar novos Arquivos:",
                         min_value=100, max_value=5000, value=st.session_state.slider_chunk,
                         step=100, key='slider_chunk')
    elif type == 'overlap':
        return st.slider("🔄 Tamanho de Sobreposição (Overlap) entre Chunks:",
                         min_value=0, max_value=1000, value=st.session_state.slider_overlap,
                         step=50, key='slider_overlap')
    else:
        return st.slider("🔍 Quantidade de Documentos Relevantes Retornados:",
                         min_value=1, max_value=15, value=st.session_state.slider_docs,
                         step=1, key='slider_docs')



def pre_loaded(type=''):
    if type == 'emb':
        return st.selectbox("🔍 Embeddings Pré-carregados:", options=list(embedding_models_carregados.keys()), index=0)
    else:
        return st.selectbox("🔍 Divisões Processadas Disponíveis:", options=list(tipo_chunk.keys()), index=0)


def loading_vector_Store(embeddings_carregados, preloaded):
    if embeddings_carregados == 'Embedding 1':
        return preloaded['faiss_vector1']
    elif embeddings_carregados == 'Embedding 2':
        return preloaded['faiss_vector2']
    elif embeddings_carregados == 'Embedding 3':
        return preloaded['faiss_vector3']


# Define o template do prompt com placeholders para "company" e "question"
prompt_template = PromptTemplate(
    input_variables=["company", "question"],
    template="""
Você é um assistente de análise financeira. Com base nos dados disponíveis, responda de forma clara e objetiva à seguinte pergunta:

Empresa: {company}
Pergunta: {question}
"""
)


def main():
    preloaded = st.session_state.preloaded_vector_store
    
    with st.sidebar:
        if st.button('Limpar Conversas'):
            st.session_state.messages = []
            
        st.subheader('⚙️ Configurações')
        own_docs_search = st.toggle('Tipo de resposta')
        if own_docs_search:
            st.success('Obtendo respostas somente do documento a ser carregado')
        else:
            st.success('Obtendo respostas do dataset pré-carregado')
        
        selected_llm = add_new_files('llms')
        selected_embedding = add_new_files()
        
        embeddings_carregados = pre_loaded('emb')
        vector_list = loading_vector_Store(embeddings_carregados, preloaded)
        if vector_list is None:
            st.warning("⚠️ Nenhum vetor carregado. O chatbot pode não funcionar corretamente.")
        else:
            st.session_state.vector_store = vector_list
            
        escolher_chunks_carregados = pre_loaded()
        chunk_size = add_new_configs_for_files('chunk')
        overlap = add_new_configs_for_files('overlap')
        search_slider = add_new_configs_for_files()
        
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
    
    # Área principal de entrada de perguntas
    user_question = st.text_input("💬 Digite sua pergunta e pressione Enter", key="user_question")
    company_name = st.text_input("🏢 Digite o nome da empresa para a pergunta padrão", key="company_name")
    
    default_question = st.selectbox(
        "Ou escolha uma pergunta padrão:",
        [
            "Qual é o objetivo da oferta primária da empresa {company}?",
            "Quais são os principais riscos associados ao investimento nas ações da empresa {company}?",
            "O que são Ações Adicionais na oferta {company}?",
            "Como a empresa pretende alocar os recursos arrecadados com a oferta primária {company}?",
            "Quais fatores podem influenciar a variação do preço das ações da empresa após a oferta {company}?",
            "O que acontece se os recursos arrecadados forem inferiores ao esperado {company}?",
            "Quais são as principais diferenças entre a oferta primária e a oferta secundária de ações {company}? Como cada uma impacta os acionistas e a empresa {company}?",
            "Quais são os riscos associados a investimentos em empresas que realizam IPOs e como os investidores podem mitigá-los {company}?",
        ],
        key='default_question'
    )
    
    # Botão para enviar a pergunta padrão com a substituição do placeholder
    if st.button("Enviar Pergunta Padrão", key="submit_default"):
        if company_name:
            user_question = default_question.replace("{company}", company_name)
        else:
            st.warning("Por favor, insira o nome da empresa.")
    
    if user_question:
        # Exibe o histórico de conversas
        for i, (question, answer) in enumerate(st.session_state.messages):
            message(question, is_user=True, key=f"user_{i}")
            message(answer, is_user=False, key=f"bot_{i}")
        
        chat_history = [(q, a) for q, a in st.session_state.messages]
        
        # Formata o prompt utilizando o template definido
        formatted_question = prompt_template.format(
            company=company_name if company_name else "N/A",
            question=user_question
        )
        
        # Seleciona o vector store e cria a cadeia de conversação conforme o tipo de resposta
        if not own_docs_search:
            st.session_state.conversational = chatbot.create_conversation_chain(
                vectorstore=st.session_state.vector_store,
                model_name=llm_models[selected_llm],
                search_model_kargs=search_slider,
                chunk_type=tipo_chunk[escolher_chunks_carregados]
            )
        else:
            if st.session_state.new_vector_store is not None:
                st.session_state.conversational = chatbot.create_conversation_chain(
                    vectorstore=st.session_state.new_vector_store,
                    model_name=llm_models[selected_llm],
                    search_model_kargs=search_slider,
                    chunk_type=tipo_chunk[escolher_chunks_carregados]
                )
            else:
                st.error("Processe um arquivo primeiro para usar a função de responder somente a texto carregado")
        
        # Executa a cadeia com o prompt já formatado
        response = st.session_state.conversational({'question': formatted_question, 'chat_history': chat_history})
        st.session_state.messages.append((formatted_question, response['answer']))
        
        message(formatted_question, is_user=True, key=f"user_{len(st.session_state.messages)}")
        message(response['answer'], is_user=False, key=f"bot_{len(st.session_state.messages)}")
        

if __name__ == '__main__':
    main()
