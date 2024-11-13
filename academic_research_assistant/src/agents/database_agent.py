# src/agents/database_agent.py
from ..database.neo4j_client import Neo4jClient

class DatabaseAgent:
    def __init__(self):
        self.db_client = Neo4jClient()

    def store_paper(self, paper_data):
        # Store a new paper in the database
        result = self.db_client.store_paper(paper_data)
        return result

    def get_papers_by_ids(self, paper_ids):
        papers = []
        for paper_id in paper_ids:
            paper = self.db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        return papers

    def __del__(self):
        self.db_client.close()
