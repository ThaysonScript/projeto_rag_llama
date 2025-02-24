
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from utils.dictionaries import embedding_models


def load_embeddings():
    embedding_list = []

    # embedding_list.append(
    #     HuggingFaceEmbeddings(model_name=embedding_models['all-MiniLM-L6-v2'])
    # )
    # embedding_list.append(
    #     HuggingFaceEmbeddings(model_name=embedding_models['all-mpnet-base-v2'])
    #     )
    # embedding_list.append(
    #     HuggingFaceEmbeddings(model_name=embedding_models['multi-qa-MiniLM-L6-cos-v1'])
    # )
    
    for embedding in embedding_models:
        embedding_list.append(
            HuggingFaceEmbeddings(model_name=embedding_models[embedding])
        )
    
    return embedding_list


def create_vectorstore(chunks, model=embedding_models['all-MiniLM-L6-v2']):
    embeddings = HuggingFaceEmbeddings(model_name=model)

    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    return vector_store


def create_conversation_chain(vectorstore, model_name='llama3-8b-8192', search_model_kargs=1, chunk_type=0):
    print(f'Dentro do chain: {vectorstore}')
    llm = ChatGroq(model=model_name)
    memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)
    
    if isinstance(vectorstore, list):
        retriever = vectorstore[chunk_type].as_retriever(search_type="similarity", search_kwargs={"k": search_model_kargs})
    else:
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": search_model_kargs})
        
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
    )
    
    return conversation_chain