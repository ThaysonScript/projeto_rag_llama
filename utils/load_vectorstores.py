import os
from langchain_community.vectorstores import FAISS
import torch
from utils.chatbot import load_embeddings


base_dir = 'embeddings_salvos'
# Criar listas para armazenar os índices carregados
faiss1_list_loaded = []
faiss2_list_loaded = []
faiss3_list_loaded = []
embedding_list = load_embeddings()

def load_vector_store():
    # Carregar os índices FAISS da pasta especificada
    for i in range(0, 3):
        print(i)
        faiss_index = FAISS.load_local(os.path.join(base_dir, f"faiss_indexes1/faiss1_index_{i}"), embedding_list[0], allow_dangerous_deserialization=True)
        faiss1_list_loaded.append(faiss_index)

    for i in range(0, 3):
        faiss_index = FAISS.load_local(os.path.join(base_dir, f"faiss_indexes2/faiss2_index_{i}"), embedding_list[1], allow_dangerous_deserialization=True)
        faiss2_list_loaded.append(faiss_index)

    for i in range(0, 3):
        faiss_index = FAISS.load_local(os.path.join(base_dir, f"faiss_indexes3/faiss3_index_{i}"), embedding_list[2], allow_dangerous_deserialization=True)
        faiss3_list_loaded.append(faiss_index)

    # Corrigir as mensagens de log para refletir corretamente os diretórios
    print(f"Todos os índices FAISS 1 foram carregados na pasta '{base_dir}/faiss1_list_pkl' com sucesso!")
    print(f"Todos os índices FAISS 2 foram carregados na pasta '{base_dir}/faiss2_list_pkl' com sucesso!")
    print(f"Todos os índices FAISS 3 foram carregados na pasta '{base_dir}/faiss3_list_pkl' com sucesso!")
    
    return {
        'faiss_vector1': faiss1_list_loaded,
        'faiss_vector2': faiss2_list_loaded,
        'faiss_vector3': faiss3_list_loaded        
    }
