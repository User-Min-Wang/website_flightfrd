from celery import Celery
from app.services import ADSBService
from extensions import db
from app.models import Aircraft
import logging


# Initialize logger
logger = logging.getLogger(__name__)


def make_celery(app):
    """Factory function to create celery instance"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

    global celery  # Declare celery as global so we can assign to it
    celery = make_celery(app)

# Initialize ADS-B service for tasks
adsb_service = ADSBService()


@celery.task
def fetch_adsb_data_task(icao_codes=None):
@celery.task
def fetch_adsb_data_task(icao_codes=None):
    """
    Periodic task to fetch ADS-B data for aircraft
    
    Args:
        icao_codes: List of specific ICAO codes to fetch (optional)
        
    Returns:
        dict: Result of ADS-B data fetch
    """
    try:
        logger.info(f"Starting ADS-B data fetch for {'all aircraft' if icao_codes is None else f'aircraft: {icao_codes}'}")
        
        # Fetch current states from ADS-B
        result = adsb_service.fetch_current_states(icao_codes)
        
        logger.info(f"Successfully fetched ADS-B data for {len(result.get('states', []))} aircraft")
        
        return {
            'status': 'success',
            'fetched_count': len(result.get('states', [])),
            'icao_codes': icao_codes
        }
        
    except Exception as e:
        logger.error(f"Error in fetch_adsb_data_task: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }


@celery.task
def fetch_adsb_data_task(icao_codes=None):
def fetch_all_aircraft_data():
    """
    Periodic task to fetch ADS-B data for all tracked aircraft
    
    Returns:
        dict: Result of ADS-B data fetch
    """
    try:
        logger.info("Starting ADS-B data fetch for all tracked aircraft")
        
        # Get all tracked aircraft ICAO codes
        all_aircraft = Aircraft.query.with_entities(Aircraft.icao_code).all()
        icao_codes = [aircraft.icao_code for aircraft in all_aircraft if aircraft.icao_code]
        
        if not icao_codes:
            logger.info("No tracked aircraft found")
            return {
                'status': 'info',
                'message': 'No tracked aircraft found'
            }
        
        # Fetch data for all tracked aircraft
        result = adsb_service.fetch_current_states(icao_codes)
        
        logger.info(f"Successfully fetched ADS-B data for {len(result.get('states', []))} tracked aircraft")
        
        return {
            'status': 'success',
            'fetched_count': len(result.get('states', [])),
            'tracked_count': len(icao_codes)
        }
        
    except Exception as e:
        logger.error(f"Error in fetch_all_aircraft_data: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }


@celery.task
def fetch_adsb_data_task(icao_codes=None):
def cleanup_old_positions():
    """
    Periodic task to clean up old flight position records
    
    Returns:
        dict: Result of cleanup operation
    """
    try:
        from datetime import datetime, timedelta
        from app.models import FlightPosition
        
        logger.info("Starting cleanup of old flight position records")
        
        # Define retention period (e.g., keep only last 7 days)
        retention_days = 7
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        # Count records to be deleted
        old_records_count = FlightPosition.query.filter(
            FlightPosition.timestamp < cutoff_date
        ).count()
        
        if old_records_count == 0:
            logger.info("No old position records to clean up")
            return {
                'status': 'info',
                'message': 'No old records to clean up'
            }
        
        # Delete old records
        deleted_count = db.session.query(FlightPosition).filter(
            FlightPosition.timestamp < cutoff_date
        ).delete(synchronize_session=False)
        
        db.session.commit()
        
        logger.info(f"Cleaned up {deleted_count} old flight position records")
        
        return {
            'status': 'success',
            'deleted_count': deleted_count,
            'retention_days': retention_days
        }
        
    except Exception as e:
        logger.error(f"Error in cleanup_old_positions: {str(e)}")
        db.session.rollback()
        return {
            'status': 'error',
            'message': str(e)
        }