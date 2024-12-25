import os
import logging
from datetime import datetime
import pytz
from sqlalchemy import create_engine, Column, Integer, Numeric, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the base for SQLAlchemy models
Base = declarative_base()

def get_current_est_time():
    """Get the current time in EST."""
    est = pytz.timezone('US/Eastern')
    return datetime.now(est)

class Sensors(Base):
    __tablename__ = 'SensorsData'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TimeStamp = Column(DateTime, default=get_current_est_time)
    Temperature = Column(Numeric)
    Gas = Column(Numeric)
    Humidity = Column(Numeric)
    Pressure = Column(Numeric)
    Altitude = Column(Numeric)
    Luminosity = Column(Numeric)
    soil_moisture = Column(Numeric)
    soil_temperature = Column(Numeric)

def setup_database(data_folder: str, db_name: str) -> sessionmaker:
    """Set up the database engine and return a sessionmaker."""
    # Ensure the data folder exists
    if not os.path.exists(data_folder):
        try:
            os.makedirs(data_folder)
            logging.info(f"Created folder: {data_folder}")
        except Exception as e:
            logging.error(f"Failed to create folder {data_folder}: {e}")
            raise

    # Create database engine
    db_path = f'sqlite:///{data_folder}/{db_name}'
    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)
    logging.info(f"Database setup complete: {db_path}")
    return sessionmaker(bind=engine)

def add_test_data(session: sessionmaker) -> None:
    """Insert test data into the database."""
    try:
        test_data = Sensors(
            Temperature=75,
            Gas=100,
            Humidity=50,
            Pressure=1000,
            Altitude=1000,
            Luminosity=105,
            soil_moisture=400,
            soil_temperature=25
        )
        session.add(test_data)
        session.commit()
        logging.info("Test data added to the database.")
    except Exception as e:
        logging.error(f"Failed to add test data: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    # Configuration
    data_folder = 'data'
    db_name = 'Neutrino.db'

    # Set up the database
    Session = setup_database(data_folder, db_name)

    # Add test data
    with Session() as session:
        add_test_data(session)

if __name__ == "__main__":
    main()
