import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to the terminal
        logging.FileHandler('logs/gyani_app.log')  # Logs to a file
    ]
)

logger = logging.getLogger(__name__)
logger.info("Gyani AI Application starting up...")