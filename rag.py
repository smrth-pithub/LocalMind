import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import ollama
import os
from docx import Document as DocxDocument

_embedder = None
_client = None

def get_embedder():
    global _embedder
    if _embedder is None:
        print("Loading embedding model...")
        _embedder = SentenceTransformer('./models/all-MiniLM-L6-v2')
    return _embedder

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path="./localmind_db")
    return _client

def load_pdf(pdf_path):
    """Load a PDF and store chunks in ChromaDB"""
    collection_name = os.path.basename(pdf_path).replace('.', '_').replace(' ', '_')
    
    client = get_client()
    embedder = get_embedder()

    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(collection_name)
    
    reader = PdfReader(pdf_path)
    chunks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text.strip():
            chunks.append({"text": text, "page": i+1})
    
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk["text"]).tolist()
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            ids=[f"page_{chunk['page']}"],
            metadatas=[{"page": chunk["page"]}]
        )
    
    print(f"Loaded {len(chunks)} pages from {pdf_path}")
    return collection_name, len(chunks)

def load_docx(docx_path):
    """Load a DOCX and store chunks in ChromaDB"""
    collection_name = os.path.basename(docx_path).replace('.', '_').replace(' ', '_')
    
    client = get_client()
    embedder = get_embedder()

    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(collection_name)
    
    doc = DocxDocument(docx_path)
    chunks = []
    current_chunk = ""
    chunk_index = 0

    for para in doc.paragraphs:
        if para.text.strip():
            current_chunk += para.text + "\n"
            if len(current_chunk) > 1000:
                chunks.append({"text": current_chunk, "index": chunk_index})
                current_chunk = ""
                chunk_index += 1

    if current_chunk.strip():
        chunks.append({"text": current_chunk, "index": chunk_index})

    for chunk in chunks:
        embedding = embedder.encode(chunk["text"]).tolist()
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            ids=[f"chunk_{chunk['index']}"],
            metadatas=[{"index": chunk["index"]}]
        )

    print(f"Loaded {len(chunks)} chunks from {docx_path}")
    return collection_name, len(chunks)    

def query_document(collection_name, question, n_results=3):
    """Query the document and get LLM answer"""
    client = get_client()
    embedder = get_embedder()

    collection = client.get_collection(collection_name)
    
    question_embedding = embedder.encode(question).tolist()
    
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    
    context = "\n\n".join(results['documents'][0])
    
    prompt = f"""You are a helpful assistant. Answer the question based only on the context provided below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {question}

Answer:"""
    
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    return response['message']['content']

if __name__ == "__main__":
    pdf_path = input("Enter PDF path to test: ")
    collection_name, pages = load_pdf(pdf_path)
    print(f"Loaded {pages} pages")
    
    while True:
        question = input("Ask a question (or 'quit'): ")
        if question == 'quit':
            break
        answer = query_document(collection_name, question)
        print(f"\nAnswer: {answer}\n")