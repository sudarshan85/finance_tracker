import os
from dotenv import load_dotenv
from app.main import app

if __name__ == "__main__":
    env = os.getenv("ENVIRONMENT", "dev")
    load_dotenv(f".env.{env}" if env != "dev" else ".env")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)