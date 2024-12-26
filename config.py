import os
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
JWT_SECRET = os.getenv("JWT_SECRET", "7wXJ4kxCRWJpMQNqRVTVR3Qbc")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", 180))
LOG_FILENAME = os.getenv("LOG_FILENAME", "/tmp/zfs-resty.log")
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))

# Logger setup
logger = logging.getLogger("zfs-resty")
logger.setLevel(LOG_LEVEL)
handler = TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
