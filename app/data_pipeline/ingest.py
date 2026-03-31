from pypdf import PdfReader
from app.core.logger import logger
from app.core.exception import CustomException
import sys
import re

def clean_text(text:str)->str:
    try:
        logger.info("in the processing of cleaning the text data")
        
        #remove newlines
        text=text.replace('\n'," ")
        
        #fix multiple spaces
        text=re.sub(r'\s+',' ',text)

        #fix PDF ligatures which are embedded togather and wrongly here
        text=text.replace("ﬁ", "fi").replace("ﬀ", "ff").replace("ﬂ", "fl")

        #remoce non ascii 
        text=text.encode('ascii','ignore').decode('ascii')
        
        return text
    except Exception as e:
        logger.error(f"error has been raised the errror is {str(e)}")
        raise CustomException(str(e),sys)


def load_file(filepath:str):
    try:
        logger.info("loading the pdf AWS Well-Architected Framework Whitepaper PDF")
        reader=PdfReader(filepath)
        text=''
        for page in reader.pages:
            extracted=page.extract_text()
            if extracted:
                text=text+extracted+" "
        
        logger.info("text is successfully loaded")
        return text
    except Exception as e:
        logger.error(f"exception araised as {str(e)}")
        raise CustomException(str(e),sys)
    
