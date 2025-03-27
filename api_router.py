from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import SessionLocal, Event
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Local Events API",
    description="Find free and low-cost events in your area",
    version="1.0.0"
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/events", response_model=List[dict])
async def search_events(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[datetime] = None,
    is_free: Optional[bool] = None,
    max_price: Optional[float] = None
):
    """
    Search events with multiple filter options
    """
    query = db.query(Event)
    
    if category:
        query = query.filter(Event.category == category)
    
    if location:
        query = query.filter(Event.location == location)
    
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    
    if is_free is not None:
        query = query.filter(Event.is_free == is_free)
    
    if max_price is not None:
        query = query.filter(Event.price <= max_price)
    
    events = query.all()
    return [event.to_dict() for event in events]

@app.get("/events/{event_id}", response_model=dict)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get specific event by ID
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.to_dict()
