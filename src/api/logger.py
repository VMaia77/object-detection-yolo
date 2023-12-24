import os
import logging
import environment.environment


def create_logger():
        
    logger = logging.getLogger(f"API: {__name__}")

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        path_logs_env = os.getenv("PATH_LOG")
        path_log = os.path.join(path_logs_env if path_logs_env else 'logs')

        if not os.path.exists(path_log):
            os.mkdir(path_log)
                            
        path_api_logs = os.path.join(path_log, 'api.log')
        handler = logging.FileHandler(path_api_logs)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger