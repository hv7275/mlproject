import logging
import os
import sys
from datetime import datetime

# 1. Create the filename with .log extension
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the 'logs' directory and ensure it exists
logs_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# 3. Create the full path to the specific log file
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# 4. Configure Logging (Note the added commas)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
