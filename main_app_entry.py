import uvicorn
from api.routes import app
from database.models import init_db

def start_application():
    """
    Initialize database and start the application
    """
    # Create database tables
    init_db()
    
    # Run the application
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )

if __name__ == "__main__":
    start_application()
