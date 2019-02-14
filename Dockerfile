FROM python:3.6.8-alpine3.8

RUN pip install pyowm

WORKDIR /getweather_app
COPY getweather.py ./

CMD ["python", "getweather.py"]