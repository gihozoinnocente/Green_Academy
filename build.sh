#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Prepare static files and database
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser if flag is set
if [[ $CREATE_SUPERUSER ]];
then
  # Setting the superuser credentials
  export DJANGO_SUPERUSER_EMAIL="i.gihozo1@alustudent.com"
  export DJANGO_SUPERUSER_PASSWORD="Password123!"
  
  # Create superuser non-interactively
  python manage.py createsuperuser --no-input
fi