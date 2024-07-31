from collections import deque
import os
from django.conf import settings

def get_log_file_content():
    log_path = (os.path.join(settings.BASE_DIR, 'log'))
    log_file_path = f'{log_path}/logfile.log'
    num_lines = settings.LOG_LINES

    try:
        with open(log_file_path, 'r') as file:
            last_lines = deque(file, maxlen=num_lines)
    except (FileNotFoundError, IOError) as e:
        return f"An error occurred while reading the log file: {e}"

    return '\n'.join(reversed(last_lines))