FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV FLASK_APP app.py
ENV FLASK_DEBUG 1
ENV FLASK_DEBUG=1
CMD flask run --host=0.0.0.0