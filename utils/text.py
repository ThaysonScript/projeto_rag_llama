import re
import tempfile
import spacy, nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

nltk.download('punkt')
nltk.download('stopwords')

def process_text(files=''):
    text = ''
    
    for file in files:
        # pdf_reader = PdfReader(file)
        
        # for page in pdf_reader.pages:
        #     text += page.extract_text()
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Salvar o conteúdo do arquivo carregado no arquivo temporário
            temp_file.write(file.getbuffer())
            temp_file_path = temp_file.name
            
            
        loader = PyPDFLoader(temp_file_path)    

        docs = loader.load()
                        
        text += docs[0].page_content            
            
            
    text = normalize_text(text)
    text = remove_stopwords(text)
    text = apply_stemming(text)
    text = apply_lemmatization(text)
                    
    return text


nlp = spacy.load("pt_core_news_sm")

def normalize_text(text):
    text = text.lower()  # Converter para minúsculas
    text = re.sub(r'\s+', ' ', text)  # Remover múltiplos espaços
    text = re.sub(r'[^a-zA-Zà-úÀ-Ú0-9 ]', '', text)  # Remover caracteres especiais
    return text


def remove_stopwords(text):
    stop_words = set(stopwords.words("portuguese"))
    # Tokenizar com SpaCy em vez de NLTK
    doc = nlp(text)
    filtered_words = [token.text for token in doc if token.text.lower() not in stop_words]
    return ' '.join(filtered_words)


def apply_stemming(text):
    stemmer = PorterStemmer()
    # Tokenizar com SpaCy
    doc = nlp(text)
    tokens = [token.text for token in doc]
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(stemmed_tokens)


def apply_lemmatization(text):
    # Lematização usando SpaCy
    doc = nlp(text)
    lemmatized_words = [token.lemma_ for token in doc]
    return ' '.join(lemmatized_words)
            
            
def create_text_chunks(text, chunks, overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunks,
        chunk_overlap=overlap
    )
    
    return text_splitter.split_text(text)