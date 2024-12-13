from neo4j import GraphDatabase


class Neo4jQuery:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_all_industries(self):
        with self.driver.session() as session:
            result = session.run("MATCH (industry:Industry) RETURN industry.name AS name")
            return [record["name"] for record in result]

    def get_all_skill_categories(self):
        with self.driver.session() as session:
            result = session.run("MATCH (skillCat:SkillCategory) RETURN skillCat.name AS name")
            return [record["name"] for record in result]

    def get_industry_skills_by_year_and_category(self, industry_name, year, category):
        with self.driver.session() as session:
            result = session.run("""
            MATCH (industry:Industry {name: $industry_name})-[:IN_YEAR]->(year:Year {value: $year})
            MATCH (industry)-[:REQUIRES_SKILL]->(skill:SkillGroup)-[:FROM_CATEGORY]->(skillCat:SkillCategory {name: $category})
            RETURN skill.name AS Skill, skill.rank AS Rank, skillCat.name AS Category
            """, industry_name=industry_name, year=year, category=category)

            return [{"Skill": record["Skill"], "Rank": record["Rank"], "Category": record["Category"]}
                    for record in result]


    def get_years(self):
        with self.driver.session() as session:
            result = session.run("MATCH (y:Year) RETURN DISTINCT y.value AS year ORDER BY y.value")
            return [record["year"] for record in result]