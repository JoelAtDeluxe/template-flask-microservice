FROM python:3.7-alpine

# These steps should basically never change
WORKDIR /app

# Copy in and build libraries (infrequent changes here)
COPY dist/requirements.txt .
RUN pip install -r requirements.txt

# Add in the source code
COPY dist .

EXPOSE 80
# some guidance on using gunicorn in containers:
# https://pythonspeed.com/articles/gunicorn-in-docker/
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", \
     "--workers=2", "--threads=4", "--worker-class=gthread", \
     "-b", "0.0.0.0:80", "wsgi:app"]
