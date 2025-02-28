import logging
import sys
import json
import os

# Ensure logs directory exists


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logs."""
    
    def format(self,record):
        log_message = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        return json.dumps(log_message)
    
    
#create logger
logger = logging.getLogger("ecommerce_app")
logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(JSONFormatter())  # Always JSON format
logger.addHandler(console_handler)

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
# File Handler (Optional for Debugging)
file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(JSONFormatter())  # JSON logs in file
logger.addHandler(file_handler)

# Prevent duplicate logs
logger.propagate = False

