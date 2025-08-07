import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str = "FlammeCore", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

        # Fichier rotatif par jour
        log_path = os.path.join(LOG_DIR, "flammecore.log")
        fh = TimedRotatingFileHandler(
            filename=log_path,
            when="midnight",     # rotation à minuit
            interval=1,
            backupCount=7,       # conserve les 7 derniers jours
            encoding="utf-8",
            utc=True             # ou False si tu veux l’heure locale
        )
        fh.setLevel(level)
        fh_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger
