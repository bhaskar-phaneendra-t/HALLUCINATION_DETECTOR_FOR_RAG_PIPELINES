from app.core.logger import logger
from fastapi import APIRouter
from app.models.schema import QueryRequest
from app.core.exception import CustomException
import sys
from app.services.retrieval_service import retrive_documents
from app.services.scoring_service import compute_similarity
from app.services.llm_services import generate_response
from app.services.control_logic import handle_response
from app.services.retrieval_service import is_relevant
from app.services.web_search import search_web
import pickle

modelpkl = "data/model.pkl"
label_pkl = "data/label_encoder.pkl"

with open(modelpkl, 'rb') as f:
    model = pickle.load(f)

with open(label_pkl, 'rb') as f:
    le = pickle.load(f)

router = APIRouter()


@router.get('/')
def home():
    logger.info('home endpoint called')
    return {'message': 'api is running'}


def extract_features(response, docs, score):
    response_length = len(response) if response else 0
    num_docs = len(docs)
    avg_doc_length = sum(len(d) for d in docs) / len(docs) if docs else 0

    return [[
        score if score else 0.0,
        response_length,
        num_docs,
        avg_doc_length
    ]]


@router.post('/ask')
def ask(request: QueryRequest):
    try:
        query = request.query
        logger.info(f'received query: {query}')

        # Step 1: Retrieval
        docs = retrive_documents(query)

        # Step 2: No context
        if not docs:
            return {
                'query': query,
                'retrieved_docs': [],
                'original_response': None,
                'hallucination_score': None,
                'decision': 'NO_CONTEXT',
                'final_output': {
                    'final_answer': 'No relevant information found in knowledge base.',
                    'status': 'NO_CONTEXT'
                }
            }

        # Step 3: Out of scope
        if not is_relevant(query, docs):
            web_answer = search_web(query)

            return {
                'query': query,
                'retrieved_docs': docs,
                'original_response': None,
                'hallucination_score': None,
                'decision': 'OUT_OF_SCOPE',
                'final_output': {
                    'final_answer': web_answer,
                    'status': 'OUT_OF_SCOPE',
                    'message': 'Query not relevant to knowledge base. Showing web results'
                }
            }

        # Step 4: LLM response
        response = generate_response(query, docs)

        # Step 5: Handle LLM failure
        if not response or "ERROR" in response:
            return {
                'query': query,
                'retrieved_docs': docs,
                'original_response': None,
                'hallucination_score': None,
                'decision': 'ERROR',
                'final_output': {
                    'final_answer': response,
                    'status': 'ERROR'
                }
            }

        # Step 6: Scoring
        score = compute_similarity(response, docs)

        # Step 7: Feature extraction
        features = extract_features(response, docs, score)

        # Step 8: ML decision
        pred = model.predict(features)
        decision = le.inverse_transform(pred)[0]

        # Step 9: Control logic
        control_result = handle_response(
            query,
            docs,
            response,
            decision
        )

        # Final safety check
        if not control_result or not isinstance(control_result, dict):
            control_result = {
                'final_answer': 'System failed to generate response',
                'status': 'ERROR'
            }

        return {
            'query': query,
            'retrieved_docs': docs,
            'original_response': response,
            'hallucination_score': score,
            'decision': decision,
            'final_output': control_result
        }

    except Exception as e:
        logger.error(f'error in api as {str(e)}')
        raise CustomException(str(e), sys)