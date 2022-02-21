FROM python:3.9
ENV PYTHONBUFFERED True
ENV APP_HOME /app
COPY . ./
RUN pip install Flask gunicorn
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
