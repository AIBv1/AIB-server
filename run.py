from dotenv import load_dotenv
import uvicorn

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
