import os
import sys
import logging
from datetime import datetime


# create a log_file based on the time
LOG_FILE = f"{datetime.now().strftime('%m %d %Y %H %M %S')}.log"

# create log_folder that will contain the log_file
Log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(Log_path, exist_ok = True)

log_file_path = os.path.join(Log_path, LOG_FILE)

logging.basicConfig(filename=log_file_path,
                    format="[%(asctime)s %(lineno)d %(levelno)d %(message)s]", 
                    level=logging.INFO)


if __name__ == "__main__":
    logging.info("Logging started")