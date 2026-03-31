from fastapi import FastAPI
from app.api.routes import router
from app.core.logger import logger

app=FastAPI(title='hallucination Firewall')

@app.on_event('startup')
def start_event():
    logger.info("application started")

app.include_router(router)