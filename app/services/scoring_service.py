from sentence_transformers import SentenceTransformer
import numpy as np
from app.core.logger import logger
from app.core.exception import CustomException
import sys

model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def keyword_overlap(response,docs):
    response_words=set(response.lower().split())
    doc_words=set(' '.join(docs).lower().split())

    if len(response_words)==0:
        return 0

    overlap=len(response_words & doc_words)
    return overlap/len(response_words)


def compute_similarity(answer:str,docs:list):
    try:
        logger.info("computing similarity score ")


        if answer is None or answer.strip()=="":
            return 0
        
        if not docs or not any(doc.strip() for doc in docs):
            return 0
        
        
        docs_embedding=model.encode(docs,normalize_embeddings=True)
        answer_embedding=model.encode([answer],normalize_embeddings=True)
        similarities=np.dot(docs_embedding,answer_embedding.T).flatten()
        
        embedding_score=float(np.max(similarities))

        overlap_score=keyword_overlap(answer,docs)

        if len(answer.split())<=6:
            final_score=max(embedding_score,.7)

        else:
            final_score=(.7*embedding_score)+.3*overlap_score

        logger.info(f"embedding_score: {embedding_score}")
        logger.info(f"overlap_score: {overlap_score}")
        logger.info(f"final_score: {final_score}")

        return final_score

    except Exception as e:
        logger.error(f"error in similarity computation as {str(e)}")
        raise CustomException(str(e),sys)