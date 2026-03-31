from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
from app.core.logger import logger
from app.core.exception import CustomException
import sys

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

index=faiss.read_index('data/faiss_index.index')

with open('data/faiss_index.pkl','rb') as f:
    chunks=pickle.load(f)

def is_relevant(query,docs,threshold=.3):
    q_emb=model.encode([query],normalize_embeddings=True)
    d_emb=model.encode(docs,normalize_embeddings=True)
    scores=np.dot(d_emb,q_emb.T)

    max_score=scores.max()
    return max_score>threshold


def retrive_documents(query:str,k=5):
    try:
        logger.info('retrieving documents')

        query_embedding=model.encode([query],normalize_embeddings=True)
        
        distances,indices=index.search(np.array(query_embedding),k)
        
        results=[]

        for i,score in zip(indices[0],distances[0]):
            if i!=-1 and i<len(chunks):
                chunk=chunks[i].strip()
                if chunk and len(chunk.split())>20:
                    results.append(chunk)
        
        logger.info(f'retrieved docs:{results}')
        return results
    

    except Exception as e:
        logger.error(f"erroe in retrive {str(e)}")
        raise CustomException(str(e),sys)