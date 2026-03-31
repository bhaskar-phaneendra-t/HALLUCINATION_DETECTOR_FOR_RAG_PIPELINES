from ddgs import DDGS
from app.core.exception import CustomException
from app.core.logger import logger
import sys

def search_web(query:str):
    results=[]
    try:
        logger.info("entered the searching")
        with DDGS() as ddgs:
            for r in ddgs.text(query,max_results=5):
                title=r.get('title','')
                body=r.get('body','')
                combined=f'{title}:{body}'
                results.append(combined)

            if not results:
                return "NO RELEVANT WEB RESULTS FOUND"
            
            return "\n\n ".join(results[:3])
        
    except Exception as e:
        logger.error(f"error {str(e)}")
        raise CustomException(str(e),sys)