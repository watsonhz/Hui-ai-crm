import logging
import sys

def setup_logging():
    fmt = logging.Formatter("%(asctime)s | %(levelname)-5s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.WARNING)
    sql_logger.addHandler(handler)
    access_logger = logging.getLogger("aicrm.access")
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(handler)
    root = logging.getLogger()
    root.setLevel(logging.WARNING)
    root.addHandler(handler)
