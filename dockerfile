FROM ubuntu:21.04

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sudo apt-get update -y && \
    sudo apt-get install -y python3-pip && \    
RUN sudo apt install software-properties-common -y
RUN sudo apt install tesseract-ocr -y
RUN sudo apt install libtesseract-dev -y
RUN sudo apt-get install ffmpeg libsm6 libxext6  -y
RUN sudo apt install apache2

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
pip install --user flask
pip3 install gunicorn