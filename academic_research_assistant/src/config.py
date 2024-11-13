# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Neo4j Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Attention")

    # Model Configuration
    MODEL_NAME = "mistralai/Mistral-7B-v0.1"  # Can be changed based on compute capability
    MODEL_PATH = os.getenv("MODEL_PATH", "./models")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Search Configuration
    MAX_PAPERS = int(os.getenv("MAX_PAPERS", "50"))
    YEARS_RANGE = 5