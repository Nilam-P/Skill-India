from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    with driver.session() as session:
        result = session.run("RETURN 'Connection Successful' AS message")
        print(result.single()['message'])
    driver.close()
except Exception as e:
    print(f"Error: {e}")