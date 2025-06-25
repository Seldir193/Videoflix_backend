

release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn video_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class gevent --timeout 300 --keep-alive 5 --no-sendfile
worker: python manage.py rqworker default
