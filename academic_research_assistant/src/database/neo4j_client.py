# src/database/neo4j_client.py
from neo4j import GraphDatabase
from datetime import datetime
from ..config import Config

class Neo4jClient:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

    def close(self):
        self._driver.close()

    def store_paper(self, paper_data):
        with self._driver.session() as session:
            result = session.execute_write(self._create_paper, paper_data)
            return result

    @staticmethod
    def _create_paper(tx, paper_data):
        query = """
        MERGE (p:Paper {id: $id})
        SET p.title = $title,
            p.abstract = $abstract,
            p.published_date = $published_date,
            p.authors = $authors,
            p.url = $url
        RETURN p
        """
        result = tx.run(query, 
                       id=paper_data['id'],
                       title=paper_data['title'],
                       abstract=paper_data['abstract'],
                       published_date=paper_data['published_date'],
                       authors=paper_data['authors'],
                       url=paper_data['url'])
        return result.single()

    def get_papers_by_timeframe(self, start_year, end_year):
        with self._driver.session() as session:
            result = session.execute_read(self._get_papers_by_timeframe, start_year, end_year)
            return result

    @staticmethod
    def _get_papers_by_timeframe(tx, start_year, end_year):
        query = """
        MATCH (p:Paper)
        WHERE date(p.published_date).year >= $start_year 
        AND date(p.published_date).year <= $end_year
        RETURN p
        ORDER BY p.published_date DESC
        """
        result = tx.run(query, start_year=start_year, end_year=end_year)
        return [dict(record["p"]) for record in result]