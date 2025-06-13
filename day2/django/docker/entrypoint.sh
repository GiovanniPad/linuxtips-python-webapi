#!/usr/bin/env bash

set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

$@