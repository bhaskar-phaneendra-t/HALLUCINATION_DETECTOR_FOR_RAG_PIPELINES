from app.data_pipeline.ingest import load_file,clean_text
from app.data_pipeline.chunk import chunk_text
from app.data_pipeline.embed_store import create_vector_store
import os

if os.path.exists('data/faiss_index.index'):
    os.remove('data/faiss_index.index')

if os.path.exists('data/faiss_index.pkl'):
    os.remove('data/faiss_index.pkl')


text=load_file('data/documents/wellarchitected-framework.pdf')
text=clean_text(text)
chunks=chunk_text(text)
create_vector_store(chunks)