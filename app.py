import streamlit as st
from utils import Neo4jQuery
from dotenv import load_dotenv
import os


load_dotenv()  # Load .env file
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")


# Initialize Neo4j connection
neo4j_query = Neo4jQuery(neo4j_uri, neo4j_username, neo4j_password)

# App title and subtitle
st.title("Skill India - Personalized Learning Pathways")
st.subheader("Explore Industry Skill Requirements and Learning Paths")

# Question 1: Get a list of industries
industries = neo4j_query.get_all_industries()
selected_industry = st.selectbox("Select an Industry:", industries)

# Question 2: Ask an additional question about the year
# years = [2022, 2023, 2024]  # You can dynamically fetch this from Neo4j if needed
years = neo4j_query.get_years()
selected_year = st.selectbox("Select a Year:", years)

# Question 3: Ask for a specific skill category
categories = neo4j_query.get_all_skill_categories()
selected_category = st.selectbox("Select a Skill Category:", categories)

if selected_industry:
    st.markdown(f"### Skill Requirements for **{selected_industry}** in **{selected_year}**")

    # Fetch and display skills for the selected industry, year, and category
    skills_info = neo4j_query.get_industry_skills_by_year_and_category(
        selected_industry, selected_year, selected_category
    )

    if skills_info:
        st.write("**Skills and Ranks**:")
        skill_table_data = {
            "Skill": [skill['Skill'] for skill in skills_info],
            "Rank": [skill['Rank'] for skill in skills_info],
            "Category": [skill['Category'] for skill in skills_info]
        }
        st.table(skill_table_data)
    else:
        st.warning("No skill data found for the selected industry, year, and category.")

# Close Neo4j connection
neo4j_query.close()
