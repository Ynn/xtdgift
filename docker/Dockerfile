FROM python:3.8
LABEL maintainer="Yoann Maurel <yoann.maurel@inria.fr"

RUN apt update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*
COPY xtdgift.py server.py code2img.py example/example.txt requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip install pillow

CMD ["python","/app/server.py"]