#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    # Caminho base do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Carrega o arquivo .env da raiz do projeto
    load_dotenv(BASE_DIR / '.env')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medfinder.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
