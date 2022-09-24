import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_logfile(full_path):
    os.makedirs(full_path, exist_ok=True)
    return f'{full_path}/error.log'


def logging():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            },
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[{server_time}] {message}",
                "style": "{"
            }
        },
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "filename": get_logfile(os.path.join(ROOT_DIR, "log"))
            },
            "null": {
                "level": "DEBUG",
                "class": "logging.NullHandler"
            },

            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple"
            }
        },
        "loggers": {
            "django": {
                "handlers": ["console", "null"],
                "propagate": True,
                "level": "INFO"
            },
            "django.request": {
                "handlers": ["console", "file"],
                "level": "ERROR",
                "propagate": False
            },
            "django.security.DisallowedHost": {
                "handlers": ["null"],
                "propagate": False
            }
        }
    }
