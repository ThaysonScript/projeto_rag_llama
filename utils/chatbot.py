
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq


embedding_models = {
    'all-MiniLM-L6-v2': 'sentence-transformers/all-MiniLM-L6-v2',
    'all-mpnet-base-v2': 'sentence-transformers/all-mpnet-base-v2',
    'multi-qa-MiniLM-L6-cos-v1': 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1',
}

llm_models = {
    'Llama3-8B': 'groq/llama3-8b-8192',
    'GPT-4': 'openai/gpt-4',
    'Mistral-7B': 'mistralai/mistral-7b'
}


def load_embeddings():
    embedding_list = []

    embedding_list.append(HuggingFaceEmbeddings(model_name=embedding_models['all-MiniLM-L6-v2']))
    embedding_list.append(HuggingFaceEmbeddings(model_name=embedding_models['all-mpnet-base-v2']))
    embedding_list.append(HuggingFaceEmbeddings(model_name=embedding_models['multi-qa-MiniLM-L6-cos-v1']))
    
    return embedding_list


def create_vectorstore(chunks, model=embedding_models['all-MiniLM-L6-v2']):
    embeddings = HuggingFaceEmbeddings(model_name=model)

    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    return vector_store


def create_conversation_chain(vectorstore, model_name='llama3-8b-8192', search_model_kargs=1, chunk_type=0):
    llm = ChatGroq(model=model_name)
    
    resposta = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore[chunk_type].as_retriever(search_kwargs={"k": search_model_kargs}),
        return_source_documents=True,
    )
    
    return resposta