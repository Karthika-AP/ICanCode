#!/usr/bin/env python
import sys
import os
import subprocess
import datetime
from datetime import datetime as dt
import yaml

with open('prop.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)
if __name__ == "__main__":
    with open('prop.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, yaml.Loader)
    currentDay = dt.now().day
    currentMonth = dt.now().month
    currentYear = dt.now().year

    finalday = cfg['date']
    finalmonth = cfg['month']
    finalyear = cfg['year']
    sdate = datetime.date(currentYear, currentMonth, currentDay)
    edate = datetime.date(finalyear, finalmonth, finalday)
    if edate < sdate:
        print("end")
        path = os.path.dirname(os.path.abspath(__file__))
        item = subprocess.Popen(["delete.bat", path], shell=True, stdout=subprocess.PIPE)
        for line in item.stdout:
            print(line)
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AITestEngine.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
