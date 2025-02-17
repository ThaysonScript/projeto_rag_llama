from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_text(files=''):
    text = ''
    
    for file in files:
        pdf_reader = PdfReader(file)
        
        for page in pdf_reader.pages:
            text += page.extract_text()
                    
    return text
            
            
def create_text_chunks(text, chunks, overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunks,
        chunk_overlap=overlap
    )
    
    return text_splitter.split_text(text)