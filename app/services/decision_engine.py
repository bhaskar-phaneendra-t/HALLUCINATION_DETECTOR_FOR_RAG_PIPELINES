from app.core.logger import logger
from app.core.exception import CustomException
import sys


def get_decision(score: float):
    try:
        logger.info("making decision")

        if score is None:
            return "NO_CONTEXT"

        if score >= 0.75:
            logger.info(f"SAFE: {score}")
            return "SAFE"

        elif score >= 0.5:
            logger.info(f"WARNING: {score}")
            return "WARNING"

        else:
            logger.info(f"HALLUCINATION: {score}")
            return "HALLUCINATION"

    except Exception as e:
        logger.error(f"error in decision engine: {str(e)}")
        raise CustomException(str(e), sys)