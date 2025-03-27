from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Create base class for declarative models
Base = declarative_base()

class Event(Base):
    """
    Database model for local events
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    location = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_free = Column(Boolean, default=False)
    price = Column(Float, default=0.0)
    source_url = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    def to_dict(self):
        """
        Convert event to dictionary for API response
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'location': self.location,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_free': self.is_free,
            'price': self.price,
            'source_url': self.source_url
        }

# Database connection setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///local_events.db')
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
