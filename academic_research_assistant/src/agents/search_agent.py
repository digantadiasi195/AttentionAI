# src/agents/search_agent.py
import arxiv
from datetime import datetime, timedelta
from ..config import Config
from ..database.neo4j_client import Neo4jClient

class SearchAgent:
    def __init__(self):
        self.db_client = Neo4jClient()
        
    def search_papers(self, topic):
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * Config.YEARS_RANGE)
        
        # Search arxiv
        search = arxiv.Search(
            query=topic,
            max_results=Config.MAX_PAPERS,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in search.results():
            # Check if paper is within date range
            if start_date <= result.published <= end_date:
                paper_data = {
                    'id': result.entry_id,
                    'title': result.title,
                    'abstract': result.summary,
                    'published_date': result.published.strftime('%Y-%m-%d'),
                    'authors': [author.name for author in result.authors],
                    'url': result.pdf_url
                }
                
                # Store in database
                self.db_client.store_paper(paper_data)
                papers.append(paper_data)
                
        return papers

    def __del__(self):
        self.db_client.close()