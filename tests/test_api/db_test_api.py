from datetime import datetime

from fastapi.testclient import TestClient

from src.database.database import MySQLClient
from src.database.model import Test
from src.main import app

client = TestClient(app)

def test_db_connection():
    test = Test(0, "Description", datetime.now())
    db = MySQLClient()

