web: gunicorn restaurant_booking.wsgi --log-file -
worker: celery -A restaurant_booking worker --loglevel=info --pool=solo
