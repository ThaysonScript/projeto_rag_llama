#!/usr/bin/env bash

python3 -m venv env

echo "GROQ_API_KEY=" > .env

venv_folder="env/bin/python"

install_packages() {
    "$venv_folder" -m pip install --upgrade pip
    "$venv_folder" -m pip install "$@"
}

# Chamando a função com os pacotes desejados
install_packages streamlit streamlit-chat pypdf python-dotenv beautifulsoup4
install_packages langchain[groq] langchain-huggingface langchain langchain-community faiss-cpu langchain_core