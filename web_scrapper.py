import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from database.models import Event

class EventScraper:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def scrape_eventbrite(self, location, category=None):
        """
        Scrape free and low-cost events from Eventbrite
        """
        try:
            # Example Eventbrite search URL (this would need to be customized)
            url = f"https://www.eventbrite.com/d/{location}/free--events/"
            if category:
                url += f"--{category}/"

            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find event cards (this selector would need to match Eventbrite's current HTML)
            event_cards = soup.find_all('div', class_='event-card')
            
            events = []
            for card in event_cards:
                try:
                    event = Event(
                        title=card.find('h3').text.strip(),
                        description=card.find('p', class_='description').text.strip() if card.find('p', class_='description') else '',
                        location=location,
                        category=category or 'General',
                        start_time=self._parse_datetime(card.find('time')['datetime']),
                        is_free=True,
                        source_url=card.find('a')['href']
                    )
                    events.append(event)
                except Exception as e:
                    self.logger.error(f"Error parsing event: {e}")
            
            # Bulk insert events
            self.db_session.add_all(events)
            self.db_session.commit()
            
            return events
        
        except Exception as e:
            self.logger.error(f"Scraping error: {e}")
            return []

    def _parse_datetime(self, datetime_str):
        """
        Parse datetime string from website
        """
        try:
            return datetime.fromisoformat(datetime_str)
        except:
            return datetime.now()

def run_scraper(location='San Francisco', category=None):
    """
    Main scraper runner
    """
    logging.basicConfig(level=logging.INFO)
    
    # Create database session
    from database.models import SessionLocal
    db_session = SessionLocal()
    
    try:
        scraper = EventScraper(db_session)
        events = scraper.scrape_eventbrite(location, category)
        print(f"Scraped {len(events)} events")
    finally:
        db_session.close()
