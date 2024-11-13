# src/agents/qa_agent.py
from ..models.llm_manager import LLMManager
from ..database.neo4j_client import Neo4jClient

class QAGent:
    def __init__(self):
        self.db_client = Neo4jClient()
        self.llm_manager = LLMManager()

    def answer_question(self, question, paper_ids):
        papers = []
        for paper_id in paper_ids:
            paper = self.db_client.get_papers_by_id(paper_id)
            if paper:
                papers.append(paper)
        
        # Use LLM to answer the question based on the selected papers
        answer = self.llm_manager.answer_question(question, papers)
        return answer

    def __del__(self):
        self.db_client.close()
