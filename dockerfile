FROM ubuntu:21.04
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8080
COPY . ./
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y    
RUN apt install software-properties-common -y
RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
RUN add-apt-repository universe
RUN apt install python3-pip -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install Pillow-PIL
RUN pip install opencv-python
RUN pip install gunicorn
RUN pip install Flask 
RUN pip install -r requirements.txt
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
