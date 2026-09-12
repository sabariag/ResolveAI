from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.getenv("PORT", "8000")
ORCHESTRATOR_URL = os.getenv(
    "ORCHESTRATOR_URL",
    "http://localhost:9000"
)