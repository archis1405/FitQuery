import json
from fastapi import FastAPI
from pydantic import BaseModel
from DBOperations.dataGenerator import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from DBOperations.embeddings import Embeddings, Retrieval, GenerateSQL

app = FastAPI()

rObj = Retrieval()
sqlObj = GenerateSQL()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global queryStore 
global storeUserQuery

class UserQuery(BaseModel):
    query: str


@app.get("/")
def demoRun():

    ################## Uncomment the Code below when running First time to create Database and Embeddings ##################

     obj = CreateSyntheticData()
     obj.executor()
     embedObj = Embeddings()
     embedObj.embedding_executor()
     return {"Message" : "Embeddings have been generated and stored in DB"}

    ########################################################################################################################
    # UNCOMMENT THE CODE BELOW WHEN YOU WANT TO REGENERATE THE EMBEDDINGS AND DATABASE
    #return "Database and Embeddings already generated!"



def generateRetrievals(user_query):
    result = rObj.get_top_matches(user_query)
    finalQuery = sqlObj.generate_sql_query(user_query, result)
    print(f"Final Query Here ::: {finalQuery}")
    postProcessedQuery = sqlObj.post_process_query(finalQuery)
    queryStore = postProcessedQuery
    return postProcessedQuery


@app.post("/fetch-data")
def fetchDataFromQuery(user_query: UserQuery):
    print(f"User Query :: {user_query.query}")
    storeUserQuery = user_query.query
    sqlQuery = generateRetrievals(user_query.query)
    queryOutput = sqlObj.execute_sql_query(sqlQuery)
    tableMetadata = sqlObj.fetch_table_metadata()
    sqlObj.store_chat_history(user_query.query, sqlQuery)
    return JSONResponse(content=jsonable_encoder({"SQLQuery": sqlQuery, "FetchedData": queryOutput, "TableMetaData": tableMetadata}))


@app.get("/chat-history")
def fetchChatHistory():
    chatSaved = sqlObj.fetch_chat_history()
    return chatSaved