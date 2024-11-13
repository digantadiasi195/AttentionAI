# src/agents/future_works_agent.py
from ..models.llm_manager import LLMManager
from ..database.neo4j_client import Neo4jClient

class FutureWorksAgent:
    def __init__(self):
        self.db_client = Neo4jClient()
        self.llm_manager = LLMManager()

    def generate_future_directions(self, paper_ids):
        papers = []
        for paper_id in paper_ids:
            paper = self.db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        
        # Generate future directions using LLM
        directions = self.llm_manager.generate_future_directions(papers)
        return directions

    def __del__(self):
        self.db_client.close()
