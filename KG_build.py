from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")


class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_graph(self):
        with self.driver.session() as session:
            # Clear existing data
            session.run("MATCH (n) DETACH DELETE n")

            # Load data from CSV and create nodes and relationships
            session.run("""
            LOAD CSV WITH HEADERS FROM 'file:///skill_data.csv' AS row
            WITH row
            MERGE (industry:Industry {name: row.industry_name})
            MERGE (year:Year {value: toInteger(row.year)})
            MERGE (skill:SkillGroup {
                name: row.skill_group_name, 
                rank: toInteger(row.skill_group_rank)
            })
            MERGE (skillCat:SkillCategory {name: row.skill_group_category})
            MERGE (isicSec:IsicSection {
                name: row.isic_section_name, 
                index: row.isic_section_index
            })

            // Creating relationships
            MERGE (industry)-[:IN_YEAR]->(year)
            MERGE (industry)-[:REQUIRES_SKILL]->(skill)
            MERGE (skill)-[:FROM_CATEGORY]->(skillCat)
            MERGE (industry)-[:HAS_ISIC]->(isicSec)
            """)

    def cleanup_duplicates(self):
        with self.driver.session() as session:
            # Remove duplicate relationships
            session.run("""
            MATCH (a)-[r]->(b)
            WITH a, b, type(r) AS type, COLLECT(r) AS relationships
            WHERE SIZE(relationships) > 1
            FOREACH (r IN TAIL(relationships) | DELETE r)
            """)


if __name__ == "__main__":
    # Replace the password and other credentials as per your Neo4j setup
    kg = KnowledgeGraph(neo4j_uri, neo4j_username, neo4j_password)
    kg.create_graph()
    kg.cleanup_duplicates()
    kg.close()
