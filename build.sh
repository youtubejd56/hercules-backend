#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations using direct (non-pooler) URL if available
# Neon's connection pooler does not support Django's migration DDL transactions
if [ -n "$DIRECT_DATABASE_URL" ]; then
  DATABASE_URL=$DIRECT_DATABASE_URL python manage.py migrate
else
  python manage.py migrate
fi
