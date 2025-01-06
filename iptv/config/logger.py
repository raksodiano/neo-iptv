import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs"
MAX_LOG_AGE_DAYS = 15


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when="midnight", interval=1, backupCount=7, encoding=None, delay=False, utc=False):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)

    def doRollover(self):
        """Override to set a custom filename format with DD/MM/YYYY."""
        if self.stream:
            self.stream.close()
            self.stream = None

        # Generate the new filename with the date format
        time_suffix = time.strftime("log_%d-%m-%Y.log")
        dfn = self.rotation_filename(time_suffix)

        # Perform the log file rotation
        self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


def delete_old_logs():
    """Delete log files older than MAX_LOG_AGE_DAYS."""
    current_time = time.time()
    for filename in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, filename)
        if os.path.isfile(file_path):
            # Get the file's last modification time
            file_age_days = (current_time - os.path.getmtime(file_path)) / (60 * 60 * 24)
            if file_age_days > MAX_LOG_AGE_DAYS:
                logger.info(f"Deleting old log file: {file_path}")
                os.remove(file_path)


def setup_logger():
    """Sets up a logger with custom filename format."""
    # Ensure the 'logs' directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Delete logs older than 15 days
    delete_old_logs()

    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)  # Minimum logging level

    # Define the log message format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Initial log file path (only for the first file)
    log_file = os.path.join(LOG_DIR, "log_{}.log".format(time.strftime("%d-%m-%Y")))

    # Rotating file handler with custom filename format
    handler = CustomTimedRotatingFileHandler(
        log_file,
        when="midnight",  # Rotate at midnight
        interval=1,  # Every 1 day
        backupCount=7  # Keep logs for the last 7 days
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


logger = setup_logger()
