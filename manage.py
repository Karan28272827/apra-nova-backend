#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    # Wait for DB before running migrations or starting server
    try:
        from core.wait_for_db import wait_for_db
        wait_for_db()
    except ImportError:
        print("wait_for_db.py not found, skipping DB wait.")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
