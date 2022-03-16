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
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install easyocr
RUN pip uninstall opencv-python-headless==4.5.5.62 -y
RUN pip install opencv-python-headless==4.5.2.52
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 1 --timeout 0 app:app
