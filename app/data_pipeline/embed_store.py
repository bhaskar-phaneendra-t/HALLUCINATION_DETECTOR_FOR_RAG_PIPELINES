from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from app.core.logger import logger
from app.core.exception  import CustomException
import sys

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(chunks,save_path='data/faiss_index'):
    try:
        logger.info("creating embeddings")

        embeddings=model.encode(chunks,normalize_embeddings=True)

        dim=embeddings.shape[1]#getting the dimension length of each vector
        
        index=faiss.IndexFlatIP(dim)#creating a faiss index using L2 distance (euclidean distance) for similarity search
        
        index.add(np.array(embeddings))

        logger.info("save faiss index")
        faiss.write_index(index,save_path+'.index')
        

        logger.info('saving chunks separately')
        with open(save_path+'.pkl','wb') as f:
            pickle.dump(chunks,f)

        logger.info("vector store created and saved")

    except Exception as e:
        logger.error(f'error in embedding store as {str(e)}')
        raise CustomException(str(e),sys)