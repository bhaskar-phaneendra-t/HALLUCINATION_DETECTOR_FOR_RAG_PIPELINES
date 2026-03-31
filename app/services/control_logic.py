from app.core.logger import logger
from app.core.exception import CustomException
from app.services.llm_services import generate_response
import sys


def handle_response(query,docs,answer,decision):
    try:
        logger.info(f"handling response with decision:{decision}")

        if decision=='SAFE':
            return{
                'final_answer':answer,
                'status':'SAFE'
            }
        
        elif decision =='WARNING':
            return{
                'final_answer':answer,
                'status':'warning',
                'message':'This answer may not be fully grounded in retrived documents.'

            }
        elif decision=='HALLUCTION':
            logger.warning('Hallucination detected - regenerating response')
            new_prompt=f'''
            Answer Only from the given context.
            If the answer is not in the context, say 'I don't know'
            context:{docs}
            question:{query}
            '''

            regenerated=generate_response(new_prompt)
            return{
                'final_answer':regenerated,
                'status':'blocked or regenerated',
                'message':'initial response was hallucinated. Regenerated safely.'
            }
    except Exception as e:
        logger.error(f'error in control service {str(e)}')
        raise CustomException(str(e),sys)