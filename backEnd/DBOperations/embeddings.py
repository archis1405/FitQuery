import os
import ast
import json
import math
import pickle
import numpy as np
import mysql.connector
from openai import OpenAI
from decouple import config
from sentence_transformers import SentenceTransformer

db = mysql.connector.connect(
    host="localhost",
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    port=3306,
    database="health_fitness"
)

cursor = db.cursor()


class Embeddings:

    def __init__(self):
        return

    def createEmbeddingsTable(self):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Embeddings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                entity_type ENUM('table', 'column'),  
                table_name VARCHAR(255),              
                column_name VARCHAR(255),             
                embedding BLOB                        
            )
        """)

    def get_embedding(self, text):
        # response = openai.Embedding.create(
        #     input=text,
        #     model="text-embedding-ada-002"
        # )

        model = SentenceTransformer("moka-ai/m3e-base")
        textEmbeddings = model.encode(text)
        return textEmbeddings.tolist()

    # Serialize embedding using pickle
    def serialize_embedding(self, embedding):
        return pickle.dumps(embedding)

    # Insert embeddings into MySQL
    def insert_embedding(self, entity_type, table_name, column_name, embedding):
        cursor.execute("""
            INSERT INTO Embeddings (entity_type, table_name, column_name, embedding)
            VALUES (%s, %s, %s, %s)
        """, (entity_type, table_name, column_name, self.serialize_embedding(embedding)))
        db.commit()

    # Function to generate and store schema embeddings (only for tables and columns)
    def store_schema_embeddings(self, schema_info):
        for table, columns in schema_info.items():
            # Get embedding for the table
            table_embedding = self.get_embedding(f"Table: {table}")
            # Insert table-level embedding
            self.insert_embedding('table', table, None, table_embedding)

            # Get embeddings for each column
            for column in columns:
                column_embedding = self.get_embedding(
                    f"Column: {column} in {table}")
                # Insert column-level embedding
                self.insert_embedding(
                    'column', table, column, column_embedding)

    # Extract schema from MySQL (only table names and column names)
    def get_schema_info(self):
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            schema_info[table_name] = [column[0] for column in columns]

        return schema_info

    # Store schema and embeddings into MySQL
    def embedding_executor(self):
        schema_info = self.get_schema_info()
        print("Schema Info Collected Successfully!")
        self.createEmbeddingsTable()
        print("Database Created Successfully!")
        self.store_schema_embeddings(schema_info)
        print("Embeddings generated and store successfully!")


class Retrieval(Embeddings):

    def __init__(self):
        return

# Fetch all embeddings from MySQL
    def fetch_all_embeddings(self):
        cursor.execute(
            "SELECT id, entity_type, table_name, column_name, embedding FROM Embeddings")
        rows = cursor.fetchall()

        embeddings = []
        for row in rows:
            id = row[0]
            entity_type = row[1]
            table_name = row[2]
            column_name = row[3]
            embedding = pickle.loads(row[4])  # Deserialize embedding from BLOB

            embeddings.append(
                (id, entity_type, table_name, column_name, embedding))

        return embeddings

    def cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_a = np.linalg.norm(vec1)
        norm_b = np.linalg.norm(vec2)
        return dot_product / (norm_a * norm_b)

    # Retrieve schema elements based on query similarity
    def retrieve_similar_schema(self, query):
        query_embedding = self.get_embedding(query)
        embeddings = self.fetch_all_embeddings()

        similarities = []
        for row in embeddings:
            id, entity_type, table_name, column_name, embedding = row
            similarity = self.cosine_similarity(query_embedding, embedding)
            similarities.append(
                (similarity, entity_type, table_name, column_name))

        # Sort by similarity, highest first
        similarities.sort(reverse=True, key=lambda x: x[0])

        # Return top 5 most similar schema elements
        return similarities[:5]

    # Example query
    def get_top_matches(self, query):
        top_matches = self.retrieve_similar_schema(query)
        # print(top_matches)
        return top_matches


class GenerateSQL:

    def __init__(self):
        return

    def generate_sql_query(self, natural_query, relevant_schema):
        # Create a prompt with the relevant schema (table and column names)
        print(f"Relevant Schema ::{relevant_schema}")
        # schema_info = '\n'.join([f"{row[1]}: {row[2]} {row[3]}" for row in relevant_schema])
        # schema_info = relevant_schema[0]
        listOfDict = list()
        for i in range(len(relevant_schema)):
            inputDict = dict()
            inputDict["Table"] = relevant_schema[i][2]
            inputDict["Column"] = relevant_schema[i][3]
            print(inputDict)
            listOfDict.append(inputDict)

        listOfDictNew = [d for d in listOfDict if d["Column"] != None]

        for i in range(len(listOfDictNew)):
            listOfDictNew[i] = str(listOfDictNew[i])

        final_db_details = "\n".join(listOfDictNew)

        client = OpenAI(api_key=config("OPENAI_API"))

        message = [{"role": "system", "content": f"You are a helpful assistant who helps in generating SQL queries using a human input. You will be provided with Database's table name and column name. You need to generate SQL query based on natural query provided to you. \n The final query should be in format:\n 'SQL Query' : '<--Generated SQL Query-->', in a key value pair. Final response should be a json. "},
                   {
            "role": "user",
                    "content": f"Generate a SQL to answer the question : {natural_query}. \n All the Database details required are: \n {final_db_details}. Note that all the primary keys of every table are marked name as `id`.The final output should always be a single MySQL query."
        }]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=message,
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )

        return response.choices[0].message.content

    def post_process_query(self, generated_query: str):
        if generated_query.startswith("```json"):
            generated_query = generated_query[7:-3]
        try:
            query = json.loads(generated_query)["SQL Query"]
        except:
            query = ast.literal_eval(generated_query)["SQL Query"]

        return query

    def execute_sql_query(self, generated_query):
        cursor.execute(generated_query)
        res = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        # Return data as a list of dictionaries (optional)
        data = [dict(zip(column_names, row)) for row in res]

        return data

    def fetch_table_metadata(self):
        cursor.execute("""
        SELECT 
            TABLE_NAME, 
            COLUMN_NAME, 
            DATA_TYPE 
        FROM 
            INFORMATION_SCHEMA.COLUMNS 
        WHERE 
            TABLE_SCHEMA = 'health_fitness';
        """)
        result = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in result]

        return data

    def store_chat_history(self, user_query, sql_query):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_query TEXT NOT NULL,              
                sql_query TEXT NOT NULL,               
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            );
        """)
        print("Chat history table created !")

        try:
            # SQL to insert the user query, generated SQL query, and the timestamp
            insert_query = """
                INSERT INTO chat_history (user_query, sql_query)
                VALUES (%s, %s);
            """
            cursor.execute(insert_query, (user_query, sql_query))
            db.commit()

            print("Conversation history saved successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_chat_history(self):
        try:
            cursor.execute("""
                SELECT user_query, sql_query 
                    FROM chat_history
                    ORDER BY created_at DESC
                    LIMIT 5;
            """)

            results = cursor.fetchall()

            history = list()
            for row in results:
                history.append({
                    "user_query": row[0],
                    "sql_query": row[1]
                })

            return history
        except Exception as e:
            print("Exception : ", e)