from pydantic import BaseModel
# this pydantic is for the data validation and converting the raw data into 
# json into serialize form it is for default data validation for fast api

class QueryRequest(BaseModel):
    query:str