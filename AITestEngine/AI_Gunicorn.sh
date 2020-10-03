#!/bin/bash

NAME="AITestEngine"                              #Name of the application (*)
DJANGODIR=/home/kpalanisamy/AITestEngine_VTAP_Model_Nginx           # Django project directory (*)
SOCKFILE=/home/kpalanisamy/AITestEngine_VTAP_Model_Nginx/AITestEngine_VTAP.sock        # we will communicate using this unix socket (*)
USER=kpalanisamy                                      # the user to run as (*)
GROUP=webdata                                    # the group to run as (*)
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn (*)
TIME=90
DJANGO_SETTINGS_MODULE=AITestEngine.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=AITestEngine.wsgi                     # WSGI module name (*)
CLASS=gthread

echo "Starting $NAME as `whoami`"


# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn --chdir /home/kpalanisamy/AITestEngine_VTAP_Model_Nginx ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --worker-class $CLASS \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE \
   -t 6000 \
  --threads=5 \
  -b :9292
