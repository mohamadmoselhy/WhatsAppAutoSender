import logging
import os

# Create a log directory if it doesn't exist
log_directory = "log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
log_file = os.path.join(log_directory, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger(name):
    """Returns a logger instance."""
    return logging.getLogger(name)
