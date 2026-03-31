
from app.core.logger import logger
from app.core.exception import CustomException
import sys


def chunk_text(text:str,chunk_size=500,overlap=50):
    try:
        logger.info("chunking text")

        start=0

        chunks=[]

        words=text.split()

        for i in range (0,len(words),chunk_size-overlap):
            chunk=' '.join(words[i:i+chunk_size])
            chunks.append(chunk)

        logger.info(f'chunks are successfully make the size of the chunks array is {len(chunks)}')

        return chunks
    

    except Exception as e:
        logger.error(f"error in the chunking as {str(e)}")
        raise CustomException(str(e),sys)