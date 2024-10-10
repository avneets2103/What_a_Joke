import os
from dotenv import load_dotenv
from app import app

# Use absolute path to load .env
load_dotenv()

def connect_db_and_start_server():
    try:
        port = os.getenv("PORT") or 8000  # Use a fallback port if PORT isn't set
        print(f"Loaded PORT: {port}")
        print(f"Server listening on port {port}")
        app.run(
            debug=True, 
            port=int(port)  # Make sure the port is an integer
        )
    except Exception as err:
        print("App didn't launch!", err)

if __name__ == "__main__":
    connect_db_and_start_server()
